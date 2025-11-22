from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.user import User

def jwt_required_custom(fn):
    """Decorator to require JWT authentication"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or missing token', 'message': str(e)}), 401
    return wrapper

def role_required(*allowed_roles):
    """Decorator to require specific user roles"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from flask import request
            # Skip JWT verification for OPTIONS requests (CORS preflight)
            if request.method == 'OPTIONS':
                return fn(*args, **kwargs)
            
            try:
                verify_jwt_in_request()
                user_id = int(get_jwt_identity())
                user = User.get_by_id(user_id)
                
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                
                if user['user_role'] not in allowed_roles:
                    return jsonify({'error': 'Access denied', 'message': f'Required role: {", ".join(allowed_roles)}'}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Authentication error', 'message': str(e)}), 401
        return wrapper
    return decorator

def get_current_user():
    """Get current authenticated user"""
    try:
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        return User.get_by_id(user_id)
    except:
        return None

def get_user_role():
    """Get current user role from JWT"""
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        return claims.get('role', None)
    except:
        return None
