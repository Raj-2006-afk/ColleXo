"""
ColleXo - Societies Blueprint
Routes for society dashboard, profile management, and form creation
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db, User, Society, SocietyForm, FormResponse
from utils import (save_uploaded_file, delete_file, allowed_file, 
                   validate_form_schema, create_breadcrumbs)
from werkzeug.utils import secure_filename
import json

societies_bp = Blueprint('societies', __name__)


def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def society_required(f):
    """Decorator to require society role"""
    from functools import wraps
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        user = User.query.get(session['user_id'])
        if user.role != 'society':
            flash('Access denied. Society account required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@societies_bp.route('/')
@society_required
def dashboard():
    """Society dashboard homepage"""
    user = User.query.get(session['user_id'])
    society = Society.query.filter_by(user_id=user.id).first()
    
    if not society:
        flash('Society profile not found.', 'danger')
        return redirect(url_for('index'))
    
    # Get statistics
    total_forms = society.forms.count()
    active_forms = society.forms.filter_by(is_active=True).count()
    total_responses = db.session.query(FormResponse).join(SocietyForm).filter(
        SocietyForm.society_id == society.id
    ).count()
    
    # Recent forms
    recent_forms = society.forms.order_by(SocietyForm.created_at.desc()).limit(5).all()
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Dashboard', None)
    ])
    
    return render_template('societies/dashboard.html',
                         society=society,
                         total_forms=total_forms,
                         active_forms=active_forms,
                         total_responses=total_responses,
                         recent_forms=recent_forms,
                         breadcrumbs=breadcrumbs)


@societies_bp.route('/profile/edit', methods=['GET', 'POST'])
@society_required
def edit_profile():
    """Edit society profile"""
    user = User.query.get(session['user_id'])
    society = Society.query.filter_by(user_id=user.id).first()
    
    if request.method == 'POST':
        try:
            # Update basic info
            society.short_desc = request.form.get('short_desc', '').strip()
            society.long_desc = request.form.get('long_desc', '').strip()
            society.contact_phone = request.form.get('contact_phone', '').strip()
            society.faculty_incharge = request.form.get('faculty_incharge', '').strip()
            society.members_count = int(request.form.get('members_count', 0))
            
            # Update social links
            society.social_instagram = request.form.get('social_instagram', '').strip()
            society.social_twitter = request.form.get('social_twitter', '').strip()
            society.social_facebook = request.form.get('social_facebook', '').strip()
            society.social_linkedin = request.form.get('social_linkedin', '').strip()
            society.website_url = request.form.get('website_url', '').strip()
            
            # Handle logo upload
            if 'logo' in request.files:
                logo_file = request.files['logo']
                if logo_file and logo_file.filename:
                    if allowed_file(logo_file.filename, current_app.config['ALLOWED_LOGO_EXTENSIONS']):
                        # Delete old logo
                        if society.logo_path and society.logo_path != 'placeholder-logo.png':
                            delete_file(society.logo_path)
                        
                        # Save new logo
                        logo_path = save_uploaded_file(logo_file, subfolder='logos')
                        society.logo_path = logo_path
                    else:
                        flash('Invalid logo file type. Allowed: PNG, JPG, JPEG, GIF, WEBP', 'danger')
                        return redirect(url_for('societies.edit_profile'))
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('societies.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating profile.', 'danger')
            print(f"Profile update error: {e}")
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Dashboard', url_for('societies.dashboard')),
        ('Edit Profile', None)
    ])
    
    return render_template('societies/edit_profile.html', 
                         society=society,
                         breadcrumbs=breadcrumbs)


@societies_bp.route('/forms/create', methods=['GET', 'POST'])
@society_required
def create_form():
    """Create new recruitment form"""
    user = User.query.get(session['user_id'])
    society = Society.query.filter_by(user_id=user.id).first()
    
    if not society.is_approved:
        flash('Your society must be approved before creating forms.', 'warning')
        return redirect(url_for('societies.dashboard'))
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            form_schema_json = request.form.get('form_schema', '[]')
            
            # Parse and validate form schema
            form_schema = json.loads(form_schema_json)
            
            if not validate_form_schema(form_schema):
                flash('Invalid form schema. Please check your form fields.', 'danger')
                return redirect(url_for('societies.create_form'))
            
            # Optional settings
            max_submissions = request.form.get('max_submissions', None)
            if max_submissions:
                max_submissions = int(max_submissions)
            
            start_date = request.form.get('start_date', None)
            end_date = request.form.get('end_date', None)
            
            # Create form
            new_form = SocietyForm(
                society_id=society.id,
                title=title,
                description=description,
                form_schema=form_schema,
                max_submissions=max_submissions,
                start_date=start_date if start_date else None,
                end_date=end_date if end_date else None
            )
            
            db.session.add(new_form)
            db.session.commit()
            
            flash('Form created successfully!', 'success')
            return redirect(url_for('societies.view_form', form_id=new_form.id))
            
        except json.JSONDecodeError:
            flash('Invalid form schema format.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the form.', 'danger')
            print(f"Form creation error: {e}")
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Dashboard', url_for('societies.dashboard')),
        ('Create Form', None)
    ])
    
    return render_template('forms/create_form.html',
                         society=society,
                         breadcrumbs=breadcrumbs)


@societies_bp.route('/forms/<int:form_id>')
@society_required
def view_form(form_id):
    """View form details and submissions"""
    user = User.query.get(session['user_id'])
    society = Society.query.filter_by(user_id=user.id).first()
    
    form = SocietyForm.query.filter_by(id=form_id, society_id=society.id).first_or_404()
    
    # Get submissions
    page = request.args.get('page', 1, type=int)
    submissions = form.responses.order_by(FormResponse.created_at.desc()).paginate(
        page=page, 
        per_page=current_app.config['SUBMISSIONS_PER_PAGE'],
        error_out=False
    )
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Dashboard', url_for('societies.dashboard')),
        (form.title, None)
    ])
    
    return render_template('forms/submissions.html',
                         form=form,
                         society=society,
                         submissions=submissions,
                         breadcrumbs=breadcrumbs)


@societies_bp.route('/forms/<int:form_id>/toggle', methods=['POST'])
@society_required
def toggle_form(form_id):
    """Toggle form active status"""
    user = User.query.get(session['user_id'])
    society = Society.query.filter_by(user_id=user.id).first()
    
    form = SocietyForm.query.filter_by(id=form_id, society_id=society.id).first_or_404()
    
    form.is_active = not form.is_active
    db.session.commit()
    
    status = 'activated' if form.is_active else 'deactivated'
    flash(f'Form {status} successfully!', 'success')
    
    return redirect(url_for('societies.view_form', form_id=form_id))


@societies_bp.route('/forms/<int:form_id>/delete', methods=['POST'])
@society_required
def delete_form(form_id):
    """Delete form and all responses"""
    user = User.query.get(session['user_id'])
    society = Society.query.filter_by(user_id=user.id).first()
    
    form = SocietyForm.query.filter_by(id=form_id, society_id=society.id).first_or_404()
    
    try:
        db.session.delete(form)
        db.session.commit()
        flash('Form deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the form.', 'danger')
        print(f"Form deletion error: {e}")
    
    return redirect(url_for('societies.dashboard'))
