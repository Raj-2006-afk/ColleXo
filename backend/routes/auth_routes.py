from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from middleware.auth import jwt_required_custom
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    response, status_code = AuthController.register(data)
    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    response, status_code = AuthController.login(data)
    return jsonify(response), status_code

@auth_bp.route('/me', methods=['GET'])
@jwt_required_custom
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    response, status_code = AuthController.get_profile(user_id)
    return jsonify(response), status_code
