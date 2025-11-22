from models.application import Application
from models.form import Form
from models.society import Society
from models.user import User

class ApplicationController:
    @staticmethod
    def create_application(data, user_id):
        """Submit a new application"""
        try:
            form_id = data.get('form_id')
            
            if not form_id:
                return {'error': 'Form ID is required'}, 400
            
            form = Form.get_by_id(form_id)
            
            if not form:
                return {'error': 'Form not found'}, 404
            
            if form['status'] != 'published':
                return {'error': 'This form is not accepting applications'}, 400
            
            society = Society.get_by_id(form['society_id'])
            
            if not society or not society['admission_open']:
                return {'error': 'Society is not accepting applications'}, 400
            
            application = Application.create(user_id, form['society_id'], form_id)
            
            if not application:
                return {'error': 'Failed to create application'}, 500
            
            if isinstance(application, dict) and 'error' in application:
                return application, 409
            
            return {
                'message': 'Application submitted successfully',
                'application': application
            }, 201
            
        except Exception as e:
            print(f"Create application error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_my_applications(user_id, page=1, per_page=10):
        """Get all applications by the current user"""
        try:
            applications, total = Application.get_by_user(user_id, page, per_page)
            
            for app in applications:
                if app.get('application_date'):
                    app['application_date'] = app['application_date'].isoformat()
                if app.get('submitted_at'):
                    app['submitted_at'] = app['submitted_at'].isoformat()
            
            return {
                'applications': applications,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }, 200
            
        except Exception as e:
            print(f"Get my applications error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_society_applications(society_id, user_id, user_role, page=1, per_page=20, status=None):
        """Get all applications for a society"""
        try:
            society = Society.get_by_id(society_id)
            
            if not society:
                return {'error': 'Society not found'}, 404
            
            if user_role != 'admin' and society['society_head_id'] != user_id:
                return {'error': 'Unauthorized to view these applications'}, 403
            
            applications, total = Application.get_by_society(society_id, page, per_page, status)
            
            for app in applications:
                if app.get('application_date'):
                    app['application_date'] = app['application_date'].isoformat()
                if app.get('submitted_at'):
                    app['submitted_at'] = app['submitted_at'].isoformat()
            
            stats = Application.get_statistics(society_id)
            
            return {
                'applications': applications,
                'statistics': stats,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }, 200
            
        except Exception as e:
            print(f"Get society applications error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_application_by_id(application_id, user_id, user_role):
        """Get application details"""
        try:
            application = Application.get_by_id(application_id)
            
            if not application:
                return {'error': 'Application not found'}, 404
            
            if user_role == 'student' and application['user_id'] != user_id:
                return {'error': 'Unauthorized to view this application'}, 403
            
            if user_role == 'societyHead':
                society = Society.get_by_id(application['society_id'])
                if not society or society['society_head_id'] != user_id:
                    return {'error': 'Unauthorized to view this application'}, 403
            
            if application.get('application_date'):
                application['application_date'] = application['application_date'].isoformat()
            if application.get('submitted_at'):
                application['submitted_at'] = application['submitted_at'].isoformat()
            
            return {'application': application}, 200
            
        except Exception as e:
            print(f"Get application error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def update_application_status(application_id, data, user_id, user_role):
        """Update application status"""
        try:
            new_status = data.get('status', '').strip()
            
            if not new_status:
                return {'error': 'Status is required'}, 400
            
            valid_statuses = ['pending', 'shortlisted', 'accepted', 'rejected']
            if new_status not in valid_statuses:
                return {'error': 'Invalid status'}, 400
            
            application = Application.get_by_id(application_id)
            
            if not application:
                return {'error': 'Application not found'}, 404
            
            if user_role == 'societyHead':
                society = Society.get_by_id(application['society_id'])
                if not society or society['society_head_id'] != user_id:
                    return {'error': 'Unauthorized to update this application'}, 403
            elif user_role != 'admin':
                return {'error': 'Unauthorized to update applications'}, 403
            
            success = Application.update_status(application_id, new_status)
            
            if not success:
                return {'error': 'Failed to update application status'}, 500
            
            updated_application = Application.get_by_id(application_id)
            
            return {
                'message': 'Application status updated successfully',
                'application': updated_application
            }, 200
            
        except Exception as e:
            print(f"Update application status error: {e}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_all_applications(page=1, per_page=20):
        """Get all applications (admin only)"""
        try:
            connection = Application.get_by_society.__globals__['get_connection']()
            if not connection:
                return {'error': 'Database connection failed'}, 500
            
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT COUNT(*) as total FROM applications")
            total = cursor.fetchone()['total']
            
            offset = (page - 1) * per_page
            
            cursor.execute("""
                SELECT a.*,
                       u.user_name, u.user_email,
                       s.society_name,
                       f.title as form_title
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                JOIN societies s ON a.society_id = s.society_id
                JOIN forms f ON a.form_id = f.form_id
                ORDER BY a.submitted_at DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            
            applications = cursor.fetchall()
            
            for app in applications:
                if app.get('application_date'):
                    app['application_date'] = app['application_date'].isoformat()
                if app.get('submitted_at'):
                    app['submitted_at'] = app['submitted_at'].isoformat()
            
            cursor.close()
            connection.close()
            
            return {
                'applications': applications,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }, 200
            
        except Exception as e:
            print(f"Get all applications error: {e}")
            return {'error': 'Internal server error'}, 500
