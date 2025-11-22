from config.db import get_connection
from mysql.connector import Error

class Society:
    @staticmethod
    def create(society_name, tagline, description, category, logo_url, 
               admission_open, admission_deadline, society_head_id):
        """Create a new society"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO societies (society_name, tagline, description, category, logo_url,
                                     admission_open, admission_deadline, society_head_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (society_name, tagline, description, category, logo_url, 
                  admission_open, admission_deadline, society_head_id))
            
            connection.commit()
            society_id = cursor.lastrowid
            return Society.get_by_id(society_id)
        except Error as e:
            print(f"Error creating society: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_id(society_id):
        """Get society by ID with head details"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT s.*, u.user_name as head_name, u.user_email as head_email
                FROM societies s
                LEFT JOIN users u ON s.society_head_id = u.user_id
                WHERE s.society_id = %s
            """, (society_id,))
            society = cursor.fetchone()
            return society
        except Error as e:
            print(f"Error fetching society: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_all(page=1, per_page=10, category=None, admission_open=None):
        """Get all societies with pagination and filters"""
        connection = get_connection()
        if not connection:
            return [], 0
        
        cursor = connection.cursor(dictionary=True)
        try:
            # Build query with filters
            where_clauses = []
            params = []
            
            if category:
                where_clauses.append("s.category = %s")
                params.append(category)
            
            if admission_open is not None:
                where_clauses.append("s.admission_open = %s")
                params.append(admission_open)
            
            where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
            
            # Get total count
            cursor.execute(f"SELECT COUNT(*) as total FROM societies s WHERE {where_sql}", params)
            total = cursor.fetchone()['total']
            
            # Get paginated results
            offset = (page - 1) * per_page
            params.extend([per_page, offset])
            
            cursor.execute(f"""
                SELECT s.*, u.user_name as head_name
                FROM societies s
                LEFT JOIN users u ON s.society_head_id = u.user_id
                WHERE {where_sql}
                ORDER BY s.created_at DESC
                LIMIT %s OFFSET %s
            """, params)
            
            societies = cursor.fetchall()
            return societies, total
        except Error as e:
            print(f"Error fetching societies: {e}")
            return [], 0
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_head(society_head_id):
        """Get society managed by a specific head"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT s.*, u.user_name as head_name
                FROM societies s
                LEFT JOIN users u ON s.society_head_id = u.user_id
                WHERE s.society_head_id = %s
            """, (society_head_id,))
            society = cursor.fetchone()
            return society
        except Error as e:
            print(f"Error fetching society: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def update(society_id, **kwargs):
        """Update society fields"""
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            # Build SET clause dynamically
            set_clauses = []
            values = []
            
            allowed_fields = ['society_name', 'tagline', 'description', 'category', 
                            'logo_url', 'member_count', 'admission_open', 'admission_deadline']
            
            for field in allowed_fields:
                if field in kwargs:
                    set_clauses.append(f"{field} = %s")
                    values.append(kwargs[field])
            
            if not set_clauses:
                return False
            
            values.append(society_id)
            query = f"UPDATE societies SET {', '.join(set_clauses)} WHERE society_id = %s"
            
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating society: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def delete(society_id):
        """Delete a society"""
        connection = get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM societies WHERE society_id = %s", (society_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting society: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
