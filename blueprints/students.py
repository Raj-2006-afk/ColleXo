"""
ColleXo - Students Blueprint
Public-facing routes for browsing societies and submitting forms
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models import db, Society, SocietyForm, FormResponse
from utils import (save_uploaded_file, allowed_file, validate_email, 
                   validate_phone, get_client_ip, create_breadcrumbs)
from sqlalchemy import or_, func
import json

students_bp = Blueprint('students', __name__)


students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('/browse')
def browse_societies():
    categories = current_app.config['SOCIETY_CATEGORIES']  # dictionary!
    return render_template('students/browse.html', categories=categories)


@students_bp.route('/societies')
def browse_societies():
    """Browse and search societies"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')  # name, views, members
    
    # Base query - only approved and active societies
    query = Society.query.filter_by(is_approved=True, is_active=True)
    
    # Apply category filter
    if category:
        query = query.filter_by(category=category)
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Society.name.like(search_term),
                Society.short_desc.like(search_term),
                Society.long_desc.like(search_term)
            )
        )
    
    # Apply sorting
    if sort_by == 'views':
        query = query.order_by(Society.views_count.desc())
    elif sort_by == 'members':
        query = query.order_by(Society.members_count.desc())
    else:
        query = query.order_by(Society.name.asc())
    
    # Paginate results
    societies = query.paginate(
        page=page,
        per_page=current_app.config['SOCIETIES_PER_PAGE'],
        error_out=False
    )
    
    # Get category counts for sidebar
    category_counts = {}
    for cat_value, cat_name in current_app.config['SOCIETY_CATEGORIES'].items():
    # your code here

        count = Society.query.filter_by(
            category=cat_value,
            is_approved=True,
            is_active=True
        ).count()
        category_counts[cat_value] = {
            'name': cat_name,
            'count': count
        }
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Browse Societies', None)
    ])
    
    return render_template('societies/browse.html',
                         societies=societies,
                         category_counts=category_counts,
                         current_category=category,
                         current_search=search,
                         current_sort=sort_by,
                         breadcrumbs=breadcrumbs)


@students_bp.route('/societies/<slug>')
def society_profile(slug):
    """View society profile page"""
    society = Society.query.filter_by(slug=slug, is_approved=True, is_active=True).first_or_404()
    
    # Increment view count
    society.views_count += 1
    db.session.commit()
    
    # Get active forms
    active_forms = society.forms.filter_by(is_active=True).order_by(
        SocietyForm.created_at.desc()
    ).all()
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Browse Societies', url_for('students.browse_societies')),
        (society.name, None)
    ])
    
    return render_template('societies/profile.html',
                         society=society,
                         active_forms=active_forms,
                         breadcrumbs=breadcrumbs)


@students_bp.route('/forms/<int:form_id>')
def view_form_public(form_id):
    """View and submit form (student view)"""
    form = SocietyForm.query.get_or_404(form_id)
    society = form.society
    
    if not society.is_approved or not society.is_active:
        flash('This society is not available.', 'danger')
        return redirect(url_for('index'))
    
    if not form.is_accepting_submissions():
        flash('This form is not currently accepting submissions.', 'warning')
        return redirect(url_for('students.society_profile', slug=society.slug))
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Browse Societies', url_for('students.browse_societies')),
        (society.name, url_for('students.society_profile', slug=society.slug)),
        (form.title, None)
    ])
    
    return render_template('forms/view_form.html',
                         form=form,
                         society=society,
                         breadcrumbs=breadcrumbs)


@students_bp.route('/forms/<int:form_id>/submit', methods=['POST'])
def submit_form(form_id):
    """Handle form submission"""
    form = SocietyForm.query.get_or_404(form_id)
    society = form.society
    
    # Validate form is accepting submissions
    if not form.is_accepting_submissions():
        flash('This form is not currently accepting submissions.', 'danger')
        return redirect(url_for('students.view_form_public', form_id=form_id))
    
    try:
        # Get submitter info
        submitter_email = request.form.get('submitter_email', '').strip().lower()
        submitter_name = request.form.get('submitter_name', '').strip()
        submitter_phone = request.form.get('submitter_phone', '').strip()
        
        # Honeypot check (anti-bot)
        honeypot = request.form.get('website', '')
        if honeypot:
            # Bot detected - silently reject
            flash('Form submitted successfully!', 'success')
            return redirect(url_for('students.submission_success', form_id=form_id))
        
        # Validate required fields
        if not submitter_email or not submitter_name:
            flash('Name and email are required.', 'danger')
            return redirect(url_for('students.view_form_public', form_id=form_id))
        
        if not validate_email(submitter_email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('students.view_form_public', form_id=form_id))
        
        if submitter_phone and not validate_phone(submitter_phone):
            flash('Invalid phone number format. Use 10 digits.', 'danger')
            return redirect(url_for('students.view_form_public', form_id=form_id))
        
        # Check for duplicate submission
        existing = FormResponse.query.filter_by(
            form_id=form_id,
            submitter_email=submitter_email
        ).first()
        
        if existing:
            flash('You have already submitted this form.', 'warning')
            return redirect(url_for('students.society_profile', slug=society.slug))
        
        # Process form fields
        form_schema = form.get_schema()
        submission_data = {}
        uploaded_files = []
        
        for field in form_schema:
            field_name = field['name']
            field_type = field['type']
            field_required = field.get('required', False)
            
            if field_type == 'file':
                # Handle file upload
                if field_name in request.files:
                    file = request.files[field_name]
                    if file and file.filename:
                        if allowed_file(file.filename, current_app.config['ALLOWED_FILE_EXTENSIONS']):
                            file_path = save_uploaded_file(file, subfolder='form_submissions')
                            uploaded_files.append({
                                'field': field_name,
                                'original_name': file.filename,
                                'stored_path': file_path
                            })
                            submission_data[field_name] = file.filename
                        else:
                            flash(f'Invalid file type for {field["label"]}', 'danger')
                            return redirect(url_for('students.view_form_public', form_id=form_id))
                    elif field_required:
                        flash(f'{field["label"]} is required.', 'danger')
                        return redirect(url_for('students.view_form_public', form_id=form_id))
            
            elif field_type == 'checkbox':
                # Handle multiple values
                values = request.form.getlist(field_name)
                submission_data[field_name] = values
                if field_required and not values:
                    flash(f'{field["label"]} is required.', 'danger')
                    return redirect(url_for('students.view_form_public', form_id=form_id))
            
            else:
                # Handle text, email, phone, textarea, select, radio
                value = request.form.get(field_name, '').strip()
                submission_data[field_name] = value
                
                if field_required and not value:
                    flash(f'{field["label"]} is required.', 'danger')
                    return redirect(url_for('students.view_form_public', form_id=form_id))
                
                # Field-specific validation
                if value:
                    if field_type == 'email' and not validate_email(value):
                        flash(f'Invalid email format for {field["label"]}', 'danger')
                        return redirect(url_for('students.view_form_public', form_id=form_id))
                    
                    if field_type == 'phone' and not validate_phone(value):
                        flash(f'Invalid phone format for {field["label"]}', 'danger')
                        return redirect(url_for('students.view_form_public', form_id=form_id))
        
        # Create form response
        response = FormResponse(
            form_id=form_id,
            submission_data=submission_data,
            submitter_email=submitter_email,
            submitter_name=submitter_name,
            submitter_phone=submitter_phone if submitter_phone else None,
            files_json=uploaded_files if uploaded_files else None,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get('User-Agent', '')[:500],
            honeypot_value=honeypot
        )
        
        db.session.add(response)
        
        # Increment form submission count
        form.submissions_count += 1
        
        db.session.commit()
        
        flash('Form submitted successfully! The society will contact you soon.', 'success')
        return redirect(url_for('students.submission_success', form_id=form_id))
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while submitting the form. Please try again.', 'danger')
        print(f"Form submission error: {e}")
        return redirect(url_for('students.view_form_public', form_id=form_id))


@students_bp.route('/forms/<int:form_id>/success')
def submission_success(form_id):
    """Form submission success page"""
    form = SocietyForm.query.get_or_404(form_id)
    society = form.society
    
    breadcrumbs = create_breadcrumbs([
        ('Home', url_for('index')),
        ('Browse Societies', url_for('students.browse_societies')),
        (society.name, url_for('students.society_profile', slug=society.slug)),
        ('Submission Successful', None)
    ])
    
    return render_template('forms/success.html',
                         form=form,
                         society=society,
                         breadcrumbs=breadcrumbs)
