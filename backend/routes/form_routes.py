from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.form import Form
from models.society import Society
from middleware.auth import jwt_required_custom, role_required

form_bp = Blueprint('form', __name__)

@form_bp.route('/published', methods=['GET'])
def get_published_forms():
    """Get all published forms (public endpoint)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        forms, total = Form.get_published(page, per_page)
        
        return jsonify({
            'forms': forms,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch forms', 'message': str(e)}), 500

@form_bp.route('/<int:form_id>', methods=['GET'])
def get_form(form_id):
    """Get form details (public endpoint)"""
    try:
        form = Form.get_by_id(form_id)
        
        if not form:
            return jsonify({'error': 'Form not found'}), 404
        
        return jsonify(form), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch form', 'message': str(e)}), 500

@form_bp.route('/', methods=['POST'], strict_slashes=False)
@form_bp.route('', methods=['POST'], strict_slashes=False)
@role_required('societyHead')
def create_form():
    """Create a new form (society head only)"""
    try:
        data = request.get_json()
        user_id = int(get_jwt_identity())
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        # Get society managed by this user
        society = Society.get_by_head(user_id)
        if not society:
            return jsonify({'error': 'No society found for this user'}), 404
        
        form = Form.create(
            society['society_id'],
            data['title'],
            data.get('status', 'draft')
        )
        
        if not form:
            return jsonify({'error': 'Failed to create form'}), 500
        
        return jsonify({
            'message': 'Form created successfully',
            'form': form
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create form', 'message': str(e)}), 500

@form_bp.route('/society/<int:society_id>', methods=['GET'])
@role_required('societyHead', 'admin')
def get_society_forms(society_id):
    """Get all forms for a society"""
    try:
        user_id = int(get_jwt_identity())
        
        # Verify ownership or admin
        from models.user import User
        current_user = User.get_by_id(user_id)
        society = Society.get_by_id(society_id)
        
        if not society:
            return jsonify({'error': 'Society not found'}), 404
        
        if current_user['user_role'] != 'admin' and society['society_head_id'] != user_id:
            return jsonify({'error': 'You are not authorized to view these forms'}), 403
        
        forms = Form.get_by_society(society_id)
        
        return jsonify({'forms': forms}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch forms', 'message': str(e)}), 500

@form_bp.route('/<int:form_id>', methods=['PUT'])
@role_required('societyHead')
def update_form(form_id):
    """Update form details"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Verify ownership
        form = Form.get_by_id(form_id)
        if not form:
            return jsonify({'error': 'Form not found'}), 404
        
        society = Society.get_by_head(user_id)
        if not society or society['society_id'] != form['society_id']:
            return jsonify({'error': 'You are not authorized to update this form'}), 403
        
        # Update form
        success = Form.update(form_id, **data)
        
        if not success:
            return jsonify({'error': 'Failed to update form'}), 500
        
        updated_form = Form.get_by_id(form_id)
        return jsonify({
            'message': 'Form updated successfully',
            'form': updated_form
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update form', 'message': str(e)}), 500

@form_bp.route('/<int:form_id>', methods=['DELETE'])
@role_required('societyHead', 'admin')
def delete_form(form_id):
    """Delete a form"""
    try:
        user_id = int(get_jwt_identity())
        
        # Verify ownership
        form = Form.get_by_id(form_id)
        if not form:
            return jsonify({'error': 'Form not found'}), 404
        
        from models.user import User
        current_user = User.get_by_id(user_id)
        
        if current_user['user_role'] != 'admin':
            society = Society.get_by_head(user_id)
            if not society or society['society_id'] != form['society_id']:
                return jsonify({'error': 'You are not authorized to delete this form'}), 403
        
        success = Form.delete(form_id)
        
        if not success:
            return jsonify({'error': 'Failed to delete form'}), 500
        
        return jsonify({'message': 'Form deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete form', 'message': str(e)}), 500
