import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return 'Password must be at least 6 characters long'
    
    if not re.search(r'[a-zA-Z]', password):
        return 'Password must contain at least one letter'
    
    return None

def validate_required_fields(data, required_fields):
    """Validate required fields in request data"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"
    
    return None
