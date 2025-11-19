"""
ColleXo - Utility Functions
Helper functions for file handling, validation, and common operations
"""
import os
import re
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
import hashlib


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_unique_filename(original_filename):
    """Generate unique filename using UUID and timestamp"""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    return f"{timestamp}_{unique_id}.{ext}"


def save_uploaded_file(file, subfolder='general'):
    """Save uploaded file and return the file path"""
    if not file:
        return None
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate secure filename
    original_filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(original_filename)
    
    # Save file
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)
    
    # Return relative path for database storage
    return os.path.join(subfolder, unique_filename)


def delete_file(file_path):
    """Delete file from uploads folder"""
    if not file_path or file_path == 'placeholder-logo.png':
        return
    
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
    
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
        except Exception as e:
            print(f"Error deleting file {full_path}: {e}")


def generate_slug(text):
    """Generate URL-friendly slug from text"""
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug[:255]  # Limit to database field length


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number format (10 digits)"""
    pattern = r'^\d{10}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None


def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    # Remove any directory path components
    filename = os.path.basename(filename)
    # Use werkzeug's secure_filename
    return secure_filename(filename)


def get_client_ip(request):
    """Get client IP address from request"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr


def hash_string(text):
    """Generate SHA256 hash of string (for duplicate detection)"""
    return hashlib.sha256(text.encode()).hexdigest()


def format_datetime(dt, format_string='%B %d, %Y at %I:%M %p'):
    """Format datetime object to readable string"""
    if not dt:
        return ''
    return dt.strftime(format_string)


def truncate_text(text, length=100, suffix='...'):
    """Truncate text to specified length"""
    if not text or len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix


def get_category_display(category_value):
    """Get display name for category"""
    categories = dict(current_app.config['SOCIETY_CATEGORIES'])
    return categories.get(category_value, category_value.title())


def validate_form_schema(schema):
    """Validate form schema structure"""
    if not isinstance(schema, list):
        return False
    
    required_fields = ['name', 'type', 'label']
    valid_types = ['text', 'email', 'phone', 'textarea', 'select', 'radio', 'checkbox', 'file']
    
    for field in schema:
        if not isinstance(field, dict):
            return False
        
        for req_field in required_fields:
            if req_field not in field:
                return False
        
        if field['type'] not in valid_types:
            return False
        
        if field['type'] in ['select', 'radio', 'checkbox']:
            if 'options' not in field or not isinstance(field['options'], list):
                return False
    
    return True


def paginate_query(query, page, per_page):
    """Paginate SQLAlchemy query"""
    return query.paginate(page=page, per_page=per_page, error_out=False)


def create_breadcrumbs(items):
    """Create breadcrumb navigation list
    items: list of tuples (title, url) where url can be None for current page
    """
    breadcrumbs = []
    for title, url in items:
        breadcrumbs.append({
            'title': title,
            'url': url,
            'active': url is None
        })
    return breadcrumbs
