import mysql.connector
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.db import get_connection

def migrate():
    """Add form questions and application responses tables"""
    connection = get_connection()
    if not connection:
        print("Failed to connect to database")
        return False
    
    cursor = connection.cursor()
    
    try:
        # Create form_questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS form_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                form_id INT NOT NULL,
                question_text TEXT NOT NULL,
                question_type ENUM('text', 'textarea', 'number', 'email', 'tel', 'select') DEFAULT 'text',
                options TEXT,
                is_required BOOLEAN DEFAULT TRUE,
                order_index INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (form_id) REFERENCES forms(form_id) ON DELETE CASCADE
            )
        """)
        print("✓ Created form_questions table")
        
        # Create application_responses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS application_responses (
                response_id INT AUTO_INCREMENT PRIMARY KEY,
                application_id INT NOT NULL,
                question_id INT NOT NULL,
                response_text TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES form_questions(question_id) ON DELETE CASCADE
            )
        """)
        print("✓ Created application_responses table")
        
        connection.commit()
        print("\n✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Starting migration: Adding questions and responses tables...")
    print("=" * 60)
    migrate()
