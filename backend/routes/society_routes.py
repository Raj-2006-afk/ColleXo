from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.society import Society
from middleware.auth import jwt_required_custom, role_required

society_bp = Blueprint('society', __name__)

@society_bp.route('/browse', methods=['GET'])
def browse_societies():
    """Browse all societies (public endpoint)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category', None)
        admission_open = request.args.get('admission_open', None, type=bool)
        
        societies, total = Society.get_all(page, per_page, category, admission_open)
        
        return jsonify({
            'societies': societies,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch societies', 'message': str(e)}), 500

@society_bp.route('/<int:society_id>', methods=['GET'])
def get_society(society_id):
    """Get society details (public endpoint)"""
    try:
        society = Society.get_by_id(society_id)
        
        if not society:
            return jsonify({'error': 'Society not found'}), 404
        
        return jsonify(society), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch society', 'message': str(e)}), 500

@society_bp.route('', methods=['POST'], strict_slashes=False)
@society_bp.route('/', methods=['POST'], strict_slashes=False)
@role_required('societyHead', 'admin')
def create_society():
    """Create a new society (society head or admin only)"""
    try:
        data = request.get_json()
        user_id = int(get_jwt_identity())
        
        # Validate required fields
        required_fields = ['society_name', 'description', 'category']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if society head already has a society
        existing = Society.get_by_head(user_id)
        if existing:
            return jsonify({'error': 'You already manage a society'}), 409
        
        society = Society.create(
            data['society_name'],
            data['tagline'],
            data['description'],
            data['category'],
            data.get('logo_url', ''),
            data.get('admission_open', True),
            data.get('admission_deadline'),
            user_id
        )
        
        if not society:
            return jsonify({'error': 'Failed to create society'}), 500
        
        return jsonify({
            'message': 'Society created successfully',
            'society': society
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to create society', 'message': str(e)}), 500

@society_bp.route('/my-society', methods=['GET'])
@role_required('societyHead')
def get_my_society():
    """Get society managed by current user"""
    try:
        user_id = int(get_jwt_identity())
        society = Society.get_by_head(user_id)
        
        if not society:
            return jsonify({'society': None, 'message': 'No society assigned yet'}), 200
        
        return jsonify({'society': society}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch society', 'message': str(e)}), 500

@society_bp.route('/<int:society_id>', methods=['PUT'])
@role_required('societyHead', 'admin')
def update_society(society_id):
    """Update society details"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Verify ownership
        society = Society.get_by_id(society_id)
        if not society:
            return jsonify({'error': 'Society not found'}), 404
        
        # Check if user is the head of this society (or admin can update any)
        from models.user import User
        current_user = User.get_by_id(user_id)
        
        if current_user['user_role'] != 'admin' and society['society_head_id'] != user_id:
            return jsonify({'error': 'You are not authorized to update this society'}), 403
        
        # Update society
        success = Society.update(society_id, **data)
        
        if not success:
            return jsonify({'error': 'Failed to update society'}), 500
        
        updated_society = Society.get_by_id(society_id)
        return jsonify({
            'message': 'Society updated successfully',
            'society': updated_society
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update society', 'message': str(e)}), 500

@society_bp.route('/<int:society_id>', methods=['DELETE'])
@role_required('admin')
def delete_society(society_id):
    """Delete a society (admin only)"""
    try:
        success = Society.delete(society_id)
        
        if not success:
            return jsonify({'error': 'Society not found or failed to delete'}), 404
        
        return jsonify({'message': 'Society deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete society', 'message': str(e)}), 500
