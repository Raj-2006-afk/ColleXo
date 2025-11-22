from models.user import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AuthController:
    @staticmethod
    def register(data):
        """Register a new user"""
        try:
            user_name = data.get('user_name', '').strip()
            user_email = data.get('user_email', '').strip().lower()
            user_password = data.get('user_password', '').strip()
            user_role = data.get('user_role', 'student')
            
            if not user_name or not user_email or not user_password:
                return {'error': 'All fields are required'}, 400
            
            if len(user_password) < 6:
                return {'error': 'Password must be at least 6 characters'}, 400
            
            if user_role not in ['student', 'societyHead', 'admin']:
                return {'error': 'Invalid user role'}, 400
            
            existing_user = User.get_by_email(user_email)
            if existing_user:
                return {'error': 'Email already registered'}, 409
            
            user = User.create(user_name, user_email, user_password, user_role)
            
            if not user:
                return {'error': 'Failed to create user'}, 500
            
            access_token = create_access_token(
                identity=str(user['user_id']),
                additional_claims={
                    'role': user['user_role'],
                    'email': user['user_email']
                },
                expires_delta=timedelta(days=7)
            )
            
            return {
                'message': 'Registration successful',
                'token': access_token,
                'user': {
                    'user_id': user['user_id'],
                    'user_name': user['user_name'],
                    'user_email': user['user_email'],
                    'user_role': user['user_role']
                }
            }, 201
            
        except Exception as e:
            print(f"Registration error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def login(data):
        """Authenticate user and return JWT token"""
        try:
            user_email = data.get('user_email', '').strip().lower()
            user_password = data.get('user_password', '').strip()
            
            if not user_email or not user_password:
                return {'error': 'Email and password are required'}, 400
            
            user = User.get_by_email(user_email)
            
            if not user:
                return {'error': 'Invalid credentials'}, 401
            
            if not User.verify_password(user_password, user['user_password']):
                return {'error': 'Invalid credentials'}, 401
            
            access_token = create_access_token(
                identity=str(user['user_id']),
                additional_claims={
                    'role': user['user_role'],
                    'email': user['user_email']
                },
                expires_delta=timedelta(days=7)
            )
            
            return {
                'message': 'Login successful',
                'token': access_token,
                'user': {
                    'user_id': user['user_id'],
                    'user_name': user['user_name'],
                    'user_email': user['user_email'],
                    'user_role': user['user_role']
                }
            }, 200
            
        except Exception as e:
            print(f"Login error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_profile(user_id):
        """Get user profile"""
        try:
            user = User.get_by_id(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'user': {
                    'user_id': user['user_id'],
                    'user_name': user['user_name'],
                    'user_email': user['user_email'],
                    'user_role': user['user_role'],
                    'created_at': user['created_at'].isoformat() if user['created_at'] else None
                }
            }, 200
            
        except Exception as e:
            print(f"Get profile error: {e}")
            return {'error': 'Internal server error'}, 500
