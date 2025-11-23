from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.application import Application
from models.society import Society
from models.form import Form
from middleware.auth import jwt_required_custom, role_required

application_bp = Blueprint('application', __name__)

@application_bp.route('/', methods=['POST'], strict_slashes=False)
@application_bp.route('', methods=['POST'], strict_slashes=False)
@role_required('student')
def create_application():
    """Submit an application (students only)"""
    try:
        data = request.get_json()
        user_id = int(get_jwt_identity())
        
        # Validate required fields
        if not data.get('form_id'):
            return jsonify({'error': 'form_id is required'}), 400
        
        # Get form details to extract society_id
        form = Form.get_by_id(data['form_id'])
        if not form:
            return jsonify({'error': 'Form not found'}), 404
        
        if form['status'] != 'published':
            return jsonify({'error': 'Form is not published'}), 400
        
        # Create application with responses
        responses = data.get('responses', {})
        application = Application.create(user_id, form['society_id'], data['form_id'], responses)
        
        if not application:
            return jsonify({'error': 'Failed to create application'}), 500
        
        if isinstance(application, dict) and 'error' in application:
            return jsonify(application), 409
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application': application
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to submit application', 'message': str(e)}), 500

@application_bp.route('/my-applications', methods=['GET'])
@role_required('student')
def get_my_applications():
    """Get all applications by current user"""
    try:
        user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        applications, total = Application.get_by_user(user_id, page, per_page)
        
        return jsonify({
            'applications': applications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch applications', 'message': str(e)}), 500

@application_bp.route('/society/<int:society_id>', methods=['GET'])
@role_required('societyHead', 'admin')
def get_society_applications(society_id):
    """Get all applications for a society"""
    try:
        user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', None)
        
        # Verify ownership or admin
        from models.user import User
        current_user = User.get_by_id(user_id)
        society = Society.get_by_id(society_id)
        
        if not society:
            return jsonify({'error': 'Society not found'}), 404
        
        if current_user['user_role'] != 'admin' and society['society_head_id'] != user_id:
            return jsonify({'error': 'You are not authorized to view these applications'}), 403
        
        applications, total = Application.get_by_society(society_id, page, per_page, status)
        
        return jsonify({
            'applications': applications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch applications', 'message': str(e)}), 500

@application_bp.route('/form/<int:form_id>', methods=['GET'])
@role_required('societyHead', 'admin')
def get_form_applications(form_id):
    """Get all applications for a form"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', None)
        
        # Verify ownership or admin
        form = Form.get_by_id(form_id)
        if not form:
            return jsonify({'error': 'Form not found'}), 404
        
        from models.user import User
        current_user = User.get_by_id(user_id)
        society = Society.get_by_id(form['society_id'])
        
        if current_user['user_role'] != 'admin' and society['society_head_id'] != user_id:
            return jsonify({'error': 'You are not authorized to view these applications'}), 403
        
        applications, total = Application.get_by_form(form_id, page, per_page, status)
        
        return jsonify({
            'applications': applications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch applications', 'message': str(e)}), 500

@application_bp.route('/<int:application_id>', methods=['GET'])
@jwt_required_custom
def get_application(application_id):
    """Get application details"""
    try:
        user_id = int(get_jwt_identity())
        
        application = Application.get_by_id(application_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify access: owner, society head, or admin
        from models.user import User
        current_user = User.get_by_id(user_id)
        society = Society.get_by_id(application['society_id'])
        
        has_access = (
            application['user_id'] == user_id or
            current_user['user_role'] == 'admin' or
            (current_user['user_role'] == 'societyHead' and society['society_head_id'] == user_id)
        )
        
        if not has_access:
            return jsonify({'error': 'You are not authorized to view this application'}), 403
        
        return jsonify(application), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch application', 'message': str(e)}), 500

@application_bp.route('/<int:application_id>/status', methods=['PUT'])
@role_required('societyHead', 'admin')
def update_application_status(application_id):
    """Update application status"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('status'):
            return jsonify({'error': 'Status is required'}), 400
        
        # Verify ownership
        application = Application.get_by_id(application_id)
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        from models.user import User
        current_user = User.get_by_id(user_id)
        society = Society.get_by_id(application['society_id'])
        
        if current_user['user_role'] != 'admin' and society['society_head_id'] != user_id:
            return jsonify({'error': 'You are not authorized to update this application'}), 403
        
        success = Application.update_status(application_id, data['status'])
        
        if not success:
            return jsonify({'error': 'Failed to update application status'}), 500
        
        updated_application = Application.get_by_id(application_id)
        return jsonify({
            'message': 'Application status updated successfully',
            'application': updated_application
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update application', 'message': str(e)}), 500

@application_bp.route('/statistics/<int:society_id>', methods=['GET'])
@role_required('societyHead', 'admin')
def get_application_statistics(society_id):
    """Get application statistics for a society"""
    try:
        user_id = int(get_jwt_identity())
        
        # Verify ownership or admin
        from models.user import User
        current_user = User.get_by_id(user_id)
        society = Society.get_by_id(society_id)
        
        if not society:
            return jsonify({'error': 'Society not found'}), 404
        
        if current_user['user_role'] != 'admin' and society['society_head_id'] != user_id:
            return jsonify({'error': 'You are not authorized to view these statistics'}), 403
        
        stats = Application.get_statistics(society_id)
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch statistics', 'message': str(e)}), 500
