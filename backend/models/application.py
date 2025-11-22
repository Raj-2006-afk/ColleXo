from config.db import get_connection
from mysql.connector import Error
from datetime import date

class Application:
    @staticmethod
    def create(user_id, society_id, form_id):
        """Create a new application"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        try:
            # Check if user already applied
            cursor.execute("""
                SELECT application_id FROM applications 
                WHERE user_id = %s AND form_id = %s
            """, (user_id, form_id))
            
            existing = cursor.fetchone()
            if existing:
                return {'error': 'Already applied to this form'}
            
            cursor.execute("""
                INSERT INTO applications (user_id, society_id, form_id, application_date)
                VALUES (%s, %s, %s, %s)
            """, (user_id, society_id, form_id, date.today()))
            
            connection.commit()
            application_id = cursor.lastrowid
            return Application.get_by_id(application_id)
        except Error as e:
            print(f"Error creating application: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_id(application_id):
        """Get application by ID with full details"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT a.*,
                       u.user_name, u.user_email,
                       s.society_name,
                       f.title as form_title
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                JOIN societies s ON a.society_id = s.society_id
                JOIN forms f ON a.form_id = f.form_id
                WHERE a.application_id = %s
            """, (application_id,))
            application = cursor.fetchone()
            return application
        except Error as e:
            print(f"Error fetching application: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_user(user_id, page=1, per_page=10):
        """Get all applications by a user"""
        connection = get_connection()
        if not connection:
            return [], 0
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM applications WHERE user_id = %s", (user_id,))
            total = cursor.fetchone()['total']
            
            # Get paginated results
            offset = (page - 1) * per_page
            
            cursor.execute("""
                SELECT a.*,
                       s.society_name, s.logo_url,
                       f.title as form_title
                FROM applications a
                JOIN societies s ON a.society_id = s.society_id
                JOIN forms f ON a.form_id = f.form_id
                WHERE a.user_id = %s
                ORDER BY a.submitted_at DESC
                LIMIT %s OFFSET %s
            """, (user_id, per_page, offset))
            
            applications = cursor.fetchall()
            return applications, total
        except Error as e:
            print(f"Error fetching user applications: {e}")
            return [], 0
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_society(society_id, page=1, per_page=20, status=None):
        """Get all applications for a society"""
        connection = get_connection()
        if not connection:
            return [], 0
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Build query with status filter
            where_clause = "a.society_id = %s"
            params = [society_id]
            
            if status:
                where_clause += " AND a.status = %s"
                params.append(status)
            
            # Get total count
            cursor.execute(f"SELECT COUNT(*) as total FROM applications a WHERE {where_clause}", params)
            total = cursor.fetchone()['total']
            
            # Get paginated results
            offset = (page - 1) * per_page
            params.extend([per_page, offset])
            
            cursor.execute(f"""
                SELECT a.*,
                       u.user_name, u.user_email,
                       f.title as form_title
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                JOIN forms f ON a.form_id = f.form_id
                WHERE {where_clause}
                ORDER BY a.submitted_at DESC
                LIMIT %s OFFSET %s
            """, params)
            
            applications = cursor.fetchall()
            return applications, total
        except Error as e:
            print(f"Error fetching society applications: {e}")
            return [], 0
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_form(form_id, page=1, per_page=20, status=None):
        """Get all applications for a form"""
        connection = get_connection()
        if not connection:
            return [], 0
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Build query with status filter
            where_clause = "a.form_id = %s"
            params = [form_id]
            
            if status:
                where_clause += " AND a.status = %s"
                params.append(status)
            
            # Get total count
            cursor.execute(f"SELECT COUNT(*) as total FROM applications a WHERE {where_clause}", params)
            total = cursor.fetchone()['total']
            
            # Get paginated results
            offset = (page - 1) * per_page
            params.extend([per_page, offset])
            
            cursor.execute(f"""
                SELECT a.*,
                       u.user_name, u.user_email
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                WHERE {where_clause}
                ORDER BY a.submitted_at DESC
                LIMIT %s OFFSET %s
            """, params)
            
            applications = cursor.fetchall()
            return applications, total
        except Error as e:
            print(f"Error fetching form applications: {e}")
            return [], 0
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def update_status(application_id, status):
        """Update application status"""
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            valid_statuses = ['pending', 'shortlisted', 'accepted', 'rejected']
            if status not in valid_statuses:
                return False
            
            cursor.execute("""
                UPDATE applications 
                SET status = %s 
                WHERE application_id = %s
            """, (status, application_id))
            
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating application status: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_statistics(society_id):
        """Get application statistics for a society"""
        connection = get_connection()
        if not connection:
            return {}
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'shortlisted' THEN 1 ELSE 0 END) as shortlisted,
                    SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) as accepted,
                    SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected
                FROM applications
                WHERE society_id = %s
            """, (society_id,))
            
            stats = cursor.fetchone()
            return stats
        except Error as e:
            print(f"Error fetching statistics: {e}")
            return {}
        finally:
            cursor.close()
            connection.close()
