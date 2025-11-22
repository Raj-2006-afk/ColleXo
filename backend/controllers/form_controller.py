from models.form import Form
from models.society import Society

class FormController:
    @staticmethod
    def get_all_forms(page=1, per_page=10):
        """Get all published forms"""
        try:
            forms, total = Form.get_published(page, per_page)
            
            for form in forms:
                if form.get('created_at'):
                    form['created_at'] = form['created_at'].isoformat()
                if form.get('published_at'):
                    form['published_at'] = form['published_at'].isoformat()
            
            return {
                'forms': forms,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }, 200
            
        except Exception as e:
            print(f"Get forms error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_form_by_id(form_id):
        """Get form details by ID"""
        try:
            form = Form.get_by_id(form_id)
            
            if not form:
                return {'error': 'Form not found'}, 404
            
            if form.get('created_at'):
                form['created_at'] = form['created_at'].isoformat()
            if form.get('published_at'):
                form['published_at'] = form['published_at'].isoformat()
            
            return {'form': form}, 200
            
        except Exception as e:
            print(f"Get form error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_forms_by_society(society_id, user_id, user_role):
        """Get all forms for a society"""
        try:
            society = Society.get_by_id(society_id)
            
            if not society:
                return {'error': 'Society not found'}, 404
            
            if user_role != 'admin' and society['society_head_id'] != user_id:
                return {'error': 'Unauthorized to view these forms'}, 403
            
            forms = Form.get_by_society(society_id)
            
            for form in forms:
                if form.get('created_at'):
                    form['created_at'] = form['created_at'].isoformat()
                if form.get('published_at'):
                    form['published_at'] = form['published_at'].isoformat()
            
            return {'forms': forms}, 200
            
        except Exception as e:
            print(f"Get society forms error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def create_form(data, user_id):
        """Create a new form"""
        try:
            society_id = data.get('society_id')
            title = data.get('title', '').strip()
            status = data.get('status', 'draft')
            
            if not society_id or not title:
                return {'error': 'Society ID and title are required'}, 400
            
            if status not in ['draft', 'published']:
                return {'error': 'Invalid status'}, 400
            
            society = Society.get_by_id(society_id)
            
            if not society:
                return {'error': 'Society not found'}, 404
            
            if society['society_head_id'] != user_id:
                return {'error': 'Unauthorized to create forms for this society'}, 403
            
            form = Form.create(society_id, title, status)
            
            if not form:
                return {'error': 'Failed to create form'}, 500
            
            return {
                'message': 'Form created successfully',
                'form': form
            }, 201
            
        except Exception as e:
            print(f"Create form error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def update_form(form_id, data, user_id):
        """Update form details"""
        try:
            form = Form.get_by_id(form_id)
            
            if not form:
                return {'error': 'Form not found'}, 404
            
            society = Society.get_by_id(form['society_id'])
            
            if not society or society['society_head_id'] != user_id:
                return {'error': 'Unauthorized to update this form'}, 403
            
            update_data = {}
            
            if 'title' in data:
                update_data['title'] = data['title'].strip()
            
            if 'status' in data:
                if data['status'] not in ['draft', 'published']:
                    return {'error': 'Invalid status'}, 400
                update_data['status'] = data['status']
            
            if not update_data:
                return {'error': 'No valid fields to update'}, 400
            
            success = Form.update(form_id, **update_data)
            
            if not success:
                return {'error': 'Failed to update form'}, 500
            
            updated_form = Form.get_by_id(form_id)
            
            return {
                'message': 'Form updated successfully',
                'form': updated_form
            }, 200
            
        except Exception as e:
            print(f"Update form error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def delete_form(form_id, user_id):
        """Delete a form"""
        try:
            form = Form.get_by_id(form_id)
            
            if not form:
                return {'error': 'Form not found'}, 404
            
            society = Society.get_by_id(form['society_id'])
            
            if not society or society['society_head_id'] != user_id:
                return {'error': 'Unauthorized to delete this form'}, 403
            
            success = Form.delete(form_id)
            
            if not success:
                return {'error': 'Failed to delete form'}, 500
            
            return {'message': 'Form deleted successfully'}, 200
            
        except Exception as e:
            print(f"Delete form error: {e}")
            return {'error': 'Internal server error'}, 500
