from models.society import Society
from models.user import User

class SocietyController:
    @staticmethod
    def get_all_societies(page=1, per_page=10, category=None, admission_open=None):
        """Get all societies with pagination and filters"""
        try:
            societies, total = Society.get_all(page, per_page, category, admission_open)
            
            for society in societies:
                if society.get('created_at'):
                    society['created_at'] = society['created_at'].isoformat()
                if society.get('admission_deadline'):
                    society['admission_deadline'] = society['admission_deadline'].isoformat()
            
            return {
                'societies': societies,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }, 200
            
        except Exception as e:
            print(f"Get societies error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_society_by_id(society_id):
        """Get society details by ID"""
        try:
            society = Society.get_by_id(society_id)
            
            if not society:
                return {'error': 'Society not found'}, 404
            
            if society.get('created_at'):
                society['created_at'] = society['created_at'].isoformat()
            if society.get('admission_deadline'):
                society['admission_deadline'] = society['admission_deadline'].isoformat()
            
            return {'society': society}, 200
            
        except Exception as e:
            print(f"Get society error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_my_society(user_id):
        """Get society managed by the current user"""
        try:
            society = Society.get_by_head(user_id)
            
            if not society:
                return {'error': 'No society found for this user'}, 404
            
            if society.get('created_at'):
                society['created_at'] = society['created_at'].isoformat()
            if society.get('admission_deadline'):
                society['admission_deadline'] = society['admission_deadline'].isoformat()
            
            return {'society': society}, 200
            
        except Exception as e:
            print(f"Get my society error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def create_society(data, user_id):
        """Create a new society"""
        try:
            society_name = data.get('society_name', '').strip()
            tagline = data.get('tagline', '').strip()
            description = data.get('description', '').strip()
            category = data.get('category', '').strip()
            logo_url = data.get('logo_url', '').strip()
            admission_open = data.get('admission_open', True)
            admission_deadline = data.get('admission_deadline')
            
            if not society_name:
                return {'error': 'Society name is required'}, 400
            
            existing = Society.get_by_head(user_id)
            if existing:
                return {'error': 'You already manage a society'}, 409
            
            society = Society.create(
                society_name, tagline, description, category,
                logo_url, admission_open, admission_deadline, user_id
            )
            
            if not society:
                return {'error': 'Failed to create society'}, 500
            
            return {
                'message': 'Society created successfully',
                'society': society
            }, 201
            
        except Exception as e:
            print(f"Create society error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def update_society(society_id, data, user_id):
        """Update society details"""
        try:
            society = Society.get_by_id(society_id)
            
            if not society:
                return {'error': 'Society not found'}, 404
            
            if society['society_head_id'] != user_id:
                return {'error': 'Unauthorized to update this society'}, 403
            
            update_data = {}
            allowed_fields = [
                'society_name', 'tagline', 'description', 'category',
                'logo_url', 'member_count', 'admission_open', 'admission_deadline'
            ]
            
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]
            
            if not update_data:
                return {'error': 'No valid fields to update'}, 400
            
            success = Society.update(society_id, **update_data)
            
            if not success:
                return {'error': 'Failed to update society'}, 500
            
            updated_society = Society.get_by_id(society_id)
            
            return {
                'message': 'Society updated successfully',
                'society': updated_society
            }, 200
            
        except Exception as e:
            print(f"Update society error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def delete_society(society_id, user_id, user_role):
        """Delete a society (admin only)"""
        try:
            if user_role != 'admin':
                return {'error': 'Only admins can delete societies'}, 403
            
            society = Society.get_by_id(society_id)
            
            if not society:
                return {'error': 'Society not found'}, 404
            
            success = Society.delete(society_id)
            
            if not success:
                return {'error': 'Failed to delete society'}, 500
            
            return {'message': 'Society deleted successfully'}, 200
            
        except Exception as e:
            print(f"Delete society error: {e}")
            return {'error': 'Internal server error'}, 500
