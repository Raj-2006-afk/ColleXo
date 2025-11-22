from flask import Blueprint, request, jsonify
from models.user import User
from models.society import Society
from middleware.auth import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@role_required('admin')
def get_all_users():
    """Get all users (admin only)"""
    try:
        role = request.args.get('role', None)
        users = User.get_all(role)
        
        # Remove passwords from response
        safe_users = []
        for user in users:
            safe_users.append({
                'user_id': user['user_id'],
                'user_name': user['user_name'],
                'user_email': user['user_email'],
                'user_role': user['user_role'],
                'created_at': user['created_at'].isoformat() if user.get('created_at') else None
            })
        
        return jsonify({'users': safe_users}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'message': str(e)}), 500

@admin_bp.route('/societies', methods=['GET'])
@role_required('admin')
def get_all_societies_admin():
    """Get all societies with full details (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        societies, total = Society.get_all(page, per_page)
        
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

@admin_bp.route('/societies/<int:society_id>/approve', methods=['PUT'])
@role_required('admin')
def approve_society(society_id):
    """Approve a society (admin only)"""
    try:
        data = request.get_json()
        
        success = Society.update(society_id, admission_open=data.get('approve', True))
        
        if not success:
            return jsonify({'error': 'Failed to update society'}), 500
        
        society = Society.get_by_id(society_id)
        return jsonify({
            'message': 'Society updated successfully',
            'society': society
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to approve society', 'message': str(e)}), 500

@admin_bp.route('/dashboard/stats', methods=['GET'])
@role_required('admin')
def get_dashboard_stats():
    """Get dashboard statistics (admin only)"""
    try:
        from config.db import get_connection
        
        connection = get_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Get total counts
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM societies")
        total_societies = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM forms WHERE status = 'published'")
        total_forms = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM applications")
        total_applications = cursor.fetchone()['total']
        
        # Get recent activities
        cursor.execute("""
            SELECT u.user_name, u.user_email, u.user_role, u.created_at
            FROM users u
            ORDER BY u.created_at DESC
            LIMIT 5
        """)
        recent_users = cursor.fetchall()
        
        cursor.execute("""
            SELECT s.society_name, s.category, s.created_at, u.user_name as head_name
            FROM societies s
            LEFT JOIN users u ON s.society_head_id = u.user_id
            ORDER BY s.created_at DESC
            LIMIT 5
        """)
        recent_societies = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_societies': total_societies,
                'total_forms': total_forms,
                'total_applications': total_applications
            },
            'recent_users': recent_users,
            'recent_societies': recent_societies
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard stats', 'message': str(e)}), 500
