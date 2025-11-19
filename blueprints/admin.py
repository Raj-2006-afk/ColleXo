"""
ColleXo - Admin Blueprint
Routes for admin panel, society approval, and platform management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db, User, Society, SocietyForm, FormResponse
from utils import create_breadcrumbs
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to require admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    # Get statistics
    total_societies = Society.query.count()
    approved_societies = Society.query.filter_by(is_approved=True).count()
    pending_societies = Society.query.filter_by(is_approved=False).count()
    total_forms = SocietyForm.query.count()
    total_submissions = FormResponse.query.count()
    total_users = User.query.count()
    
    # Recent registrations (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_registrations = Society.query.filter(
        Society.created_at >= week_ago
    ).count()
    
    # Recent submissions (last 7 days)
    recent_submissions = FormResponse.query.filter(
        FormResponse.created_at >= week_ago
    ).count()
    
    # Societies by category
    category_stats = db.session.query(
        Society.category,
        func.count(Society.id).label('count')
    ).filter_by(is_approved=True).group_by(Society.category).all()
    
    # Recent pending societies
    pending_societies_list = Society.query.filter_by(
        is_approved=False
    ).order_by(Society.created_at.desc()).limit(5).all()
    
    # Most active societies (by form submissions)
    active_societies = db.session.query(
        Society,
        func.count(FormResponse.id).label('response_count')
    ).join(SocietyForm).join(FormResponse).filter(
        Society.is_approved == True
    ).group_by(Society.id).order_by(
        func.count(FormResponse.id).desc()
    ).limit(5).all()
    
    breadcrumbs = create_breadcrumbs([
        ('Admin Panel', None)
    ])
    
    return render_template('admin/dashboard.html',
                         total_societies=total_societies,
                         approved_societies=approved_societies,
                         pending_societies=pending_societies,
                         total_forms=total_forms,
                         total_submissions=total_submissions,
                         total_users=total_users,
                         recent_registrations=recent_registrations,
                         recent_submissions=recent_submissions,
                         category_stats=category_stats,
                         pending_societies_list=pending_societies_list,
                         active_societies=active_societies,
                         breadcrumbs=breadcrumbs)


@admin_bp.route('/societies/pending')
@admin_required
def pending_societies():
    """View and manage pending society approvals"""
    page = request.args.get('page', 1, type=int)
    
    societies = Society.query.filter_by(is_approved=False).order_by(
        Society.created_at.desc()
    ).paginate(
        page=page,
        per_page=20,
        error_out=False
    )
    
    breadcrumbs = create_breadcrumbs([
        ('Admin Panel', url_for('admin.dashboard')),
        ('Pending Approvals', None)
    ])
    
    return render_template('admin/approve_societies.html',
                         societies=societies,
                         breadcrumbs=breadcrumbs)


@admin_bp.route('/societies/<int:society_id>/approve', methods=['POST'])
@admin_required
def approve_society(society_id):
    """Approve a society"""
    society = Society.query.get_or_404(society_id)
    
    society.is_approved = True
    db.session.commit()
    
    flash(f'{society.name} has been approved!', 'success')
    return redirect(url_for('admin.pending_societies'))


@admin_bp.route('/societies/<int:society_id>/reject', methods=['POST'])
@admin_required
def reject_society(society_id):
    """Reject/delete a society registration"""
    society = Society.query.get_or_404(society_id)
    
    society_name = society.name
    
    # Delete associated user account
    if society.user_id:
        user = User.query.get(society.user_id)
        if user:
            db.session.delete(user)
    
    db.session.delete(society)
    db.session.commit()
    
    flash(f'{society_name} registration has been rejected and removed.', 'info')
    return redirect(url_for('admin.pending_societies'))


@admin_bp.route('/societies')
@admin_required
def manage_societies():
    """View and manage all societies"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')  # all, approved, pending, inactive
    
    query = Society.query
    
    if status == 'approved':
        query = query.filter_by(is_approved=True, is_active=True)
    elif status == 'pending':
        query = query.filter_by(is_approved=False)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    
    societies = query.order_by(Society.created_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )
    
    breadcrumbs = create_breadcrumbs([
        ('Admin Panel', url_for('admin.dashboard')),
        ('Manage Societies', None)
    ])
    
    return render_template('admin/manage_societies.html',
                         societies=societies,
                         current_status=status,
                         breadcrumbs=breadcrumbs)


@admin_bp.route('/societies/<int:society_id>/toggle-active', methods=['POST'])
@admin_required
def toggle_society_active(society_id):
    """Toggle society active status"""
    society = Society.query.get_or_404(society_id)
    
    society.is_active = not society.is_active
    db.session.commit()
    
    status = 'activated' if society.is_active else 'deactivated'
    flash(f'{society.name} has been {status}.', 'success')
    
    return redirect(request.referrer or url_for('admin.manage_societies'))


@admin_bp.route('/societies/<int:society_id>/delete', methods=['POST'])
@admin_required
def delete_society(society_id):
    """Permanently delete a society"""
    society = Society.query.get_or_404(society_id)
    
    society_name = society.name
    
    # Delete associated user
    if society.user_id:
        user = User.query.get(society.user_id)
        if user:
            db.session.delete(user)
    
    db.session.delete(society)
    db.session.commit()
    
    flash(f'{society_name} has been permanently deleted.', 'info')
    return redirect(url_for('admin.manage_societies'))


@admin_bp.route('/forms')
@admin_required
def view_all_forms():
    """View all forms across all societies"""
    page = request.args.get('page', 1, type=int)
    
    forms = SocietyForm.query.join(Society).order_by(
        SocietyForm.created_at.desc()
    ).paginate(
        page=page,
        per_page=20,
        error_out=False
    )
    
    breadcrumbs = create_breadcrumbs([
        ('Admin Panel', url_for('admin.dashboard')),
        ('All Forms', None)
    ])
    
    return render_template('admin/view_forms.html',
                         forms=forms,
                         breadcrumbs=breadcrumbs)


@admin_bp.route('/submissions')
@admin_required
def view_all_submissions():
    """View all form submissions"""
    page = request.args.get('page', 1, type=int)
    
    submissions = FormResponse.query.join(SocietyForm).join(Society).order_by(
        FormResponse.created_at.desc()
    ).paginate(
        page=page,
        per_page=50,
        error_out=False
    )
    
    breadcrumbs = create_breadcrumbs([
        ('Admin Panel', url_for('admin.dashboard')),
        ('All Submissions', None)
    ])
    
    return render_template('admin/view_submissions.html',
                         submissions=submissions,
                         breadcrumbs=breadcrumbs)


@admin_bp.route('/users')
@admin_required
def manage_users():
    """Manage user accounts"""
    page = request.args.get('page', 1, type=int)
    role = request.args.get('role', 'all')
    
    query = User.query
    
    if role != 'all':
        query = query.filter_by(role=role)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=50,
        error_out=False
    )
    
    breadcrumbs = create_breadcrumbs([
        ('Admin Panel', url_for('admin.dashboard')),
        ('Manage Users', None)
    ])
    
    return render_template('admin/manage_users.html',
                         users=users,
                         current_role=role,
                         breadcrumbs=breadcrumbs)


@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def toggle_user_active(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deactivating themselves
    if user.id == session['user_id']:
        flash('You cannot deactivate your own account.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.email} has been {status}.', 'success')
    
    return redirect(url_for('admin.manage_users'))
