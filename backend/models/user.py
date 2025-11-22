from config.db import get_connection
from mysql.connector import Error
import bcrypt

class User:
    @staticmethod
    def create(user_name, user_email, user_password, user_role='student'):
        """Create a new user"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        try:
            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute("""
                INSERT INTO users (user_name, user_email, user_password, user_role)
                VALUES (%s, %s, %s, %s)
            """, (user_name, user_email, hashed_password, user_role))
            
            connection.commit()
            user_id = cursor.lastrowid
            return User.get_by_id(user_id)
        except Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_email(user_email):
        """Get user by email"""
        connection = get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Verify password"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def get_all(role=None, limit=50, offset=0):
        """Get all users with pagination"""
        connection = get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        try:
            if role:
                cursor.execute("""
                    SELECT user_id, user_name, user_email, user_role, created_at 
                    FROM users WHERE user_role = %s 
                    ORDER BY created_at DESC LIMIT %s OFFSET %s
                """, (role, limit, offset))
            else:
                cursor.execute("""
                    SELECT user_id, user_name, user_email, user_role, created_at 
                    FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s
                """, (limit, offset))
            users = cursor.fetchall()
            return users
        except Error as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def count(role=None):
        """Count users"""
        connection = get_connection()
        if not connection:
            return 0
        
        cursor = connection.cursor()
        try:
            if role:
                cursor.execute("SELECT COUNT(*) FROM users WHERE user_role = %s", (role,))
            else:
                cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Error counting users: {e}")
            return 0
        finally:
            cursor.close()
            connection.close()
