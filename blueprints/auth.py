"""
Authentication Blueprint - FIXED
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, User, Society
from utils import generate_slug
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    breadcrumbs = [
        {'title': 'Home', 'url': url_for('index')},
        {'title': 'Register Society', 'active': True}
    ]
    categories = ['technical', 'cultural', 'sports', 'literary', 'social_service', 'other']
    
    if request.method == 'GET':
        return render_template('auth/register.html', breadcrumbs=breadcrumbs, categories=categories)
    
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    short_desc = request.form.get('short_desc', '').strip()
    category = request.form.get('category', '')
    contact_phone = request.form.get('contact_phone', '').strip()
    
    if not all([name, email, password, confirm_password, short_desc, category]):
        flash('All required fields must be filled', 'error')
        return render_template('auth/register.html', breadcrumbs=breadcrumbs, categories=categories)
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return render_template('auth/register.html', breadcrumbs=breadcrumbs, categories=categories)
    
    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'error')
        return render_template('auth/register.html', breadcrumbs=breadcrumbs, categories=categories)
    
    if Society.query.filter_by(name=name).first():
        flash('Society name already taken', 'error')
        return render_template('auth/register.html', breadcrumbs=breadcrumbs, categories=categories)
    
    logo_filename = 'default-logo.png'
    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            logo_filename = unique_filename
    
    try:
        user = User(email=email, password_hash=generate_password_hash(password), role='society')
        db.session.add(user)
        db.session.flush()
        
        society = Society(
            user_id=user.id,
            name=name,
            slug=generate_slug(name),
            short_desc=short_desc,
            category=category,
            contact_email=email,
            contact_phone=contact_phone,
            logo_path=logo_filename,
            is_approved=False,
            is_active=True
        )
        db.session.add(society)
        db.session.commit()
        
        flash('Registration successful! Wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
        return render_template('auth/register.html', breadcrumbs=breadcrumbs, categories=categories)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    breadcrumbs = [
        {'title': 'Home', 'url': url_for('index')},
        {'title': 'Login', 'active': True}
    ]
    
    if request.method == 'GET':
        return render_template('auth/login.html', breadcrumbs=breadcrumbs)
    
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    if not email or not password:
        flash('Email and password required', 'error')
        return render_template('auth/login.html', breadcrumbs=breadcrumbs)
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        flash('Invalid credentials', 'error')
        return render_template('auth/login.html', breadcrumbs=breadcrumbs)
    
    if not user.is_active:
        flash('Account deactivated', 'error')
        return render_template('auth/login.html', breadcrumbs=breadcrumbs)
    
    session['user_id'] = user.id
    session['user_role'] = user.role
    session['user_email'] = user.email
    
    if user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif user.role == 'society':
        return redirect(url_for('societies.dashboard'))
    return redirect(url_for('index'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    breadcrumbs = [
        {'title': 'Home', 'url': url_for('index')},
        {'title': 'Forgot Password', 'active': True}
    ]
    
    if request.method == 'POST':
        flash('Password reset coming soon', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', breadcrumbs=breadcrumbs)
