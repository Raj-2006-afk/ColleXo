from config.db import get_connection
from mysql.connector import Error
from datetime import datetime

class Form:
    @staticmethod
    def create(society_id, title, status='draft'):
        """Create a new form"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        try:
            published_at = datetime.now() if status == 'published' else None
            
            cursor.execute("""
                INSERT INTO forms (society_id, title, status, published_at)
                VALUES (%s, %s, %s, %s)
            """, (society_id, title, status, published_at))
            
            connection.commit()
            form_id = cursor.lastrowid
            return Form.get_by_id(form_id)
        except Error as e:
            print(f"Error creating form: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_id(form_id):
        """Get form by ID with society details and questions"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT f.*, s.society_name, s.category, s.logo_url
                FROM forms f
                JOIN societies s ON f.society_id = s.society_id
                WHERE f.form_id = %s
            """, (form_id,))
            form = cursor.fetchone()
            
            if form:
                # Get questions for this form
                cursor.execute("""
                    SELECT * FROM form_questions
                    WHERE form_id = %s
                    ORDER BY order_index, question_id
                """, (form_id,))
                form['questions'] = cursor.fetchall()
            
            return form
        except Error as e:
            print(f"Error fetching form: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_society(society_id):
        """Get all forms for a society"""
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT f.*, 
                       (SELECT COUNT(*) FROM applications WHERE form_id = f.form_id) as application_count
                FROM forms f
                WHERE f.society_id = %s
                ORDER BY f.created_at DESC
            """, (society_id,))
            forms = cursor.fetchall()
            return forms
        except Error as e:
            print(f"Error fetching forms: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_published(page=1, per_page=10):
        """Get all published forms with pagination"""
        connection = get_connection()
        if not connection:
            return [], 0
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM forms WHERE status = 'published'")
            total = cursor.fetchone()['total']
            
            # Get paginated results
            offset = (page - 1) * per_page
            
            cursor.execute("""
                SELECT f.*, s.society_name, s.category, s.logo_url,
                       (SELECT COUNT(*) FROM applications WHERE form_id = f.form_id) as application_count
                FROM forms f
                JOIN societies s ON f.society_id = s.society_id
                WHERE f.status = 'published'
                ORDER BY f.published_at DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            
            forms = cursor.fetchall()
            return forms, total
        except Error as e:
            print(f"Error fetching published forms: {e}")
            return [], 0
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def update(form_id, **kwargs):
        """Update form fields"""
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            set_clauses = []
            values = []
            
            if 'title' in kwargs:
                set_clauses.append("title = %s")
                values.append(kwargs['title'])
            
            if 'status' in kwargs:
                set_clauses.append("status = %s")
                values.append(kwargs['status'])
                
                # Set published_at when changing to published
                if kwargs['status'] == 'published':
                    set_clauses.append("published_at = %s")
                    values.append(datetime.now())
            
            if not set_clauses:
                return False
            
            values.append(form_id)
            query = f"UPDATE forms SET {', '.join(set_clauses)} WHERE form_id = %s"
            
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating form: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def delete(form_id):
        """Delete a form"""
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM forms WHERE form_id = %s", (form_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting form: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
