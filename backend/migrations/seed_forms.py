import mysql.connector
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.db import get_connection
from datetime import datetime

def seed_forms():
    """Add recruitment forms with questions for existing societies"""
    connection = get_connection()
    if not connection:
        print("Failed to connect to database")
        return False
    
    cursor = connection.cursor()
    
    try:
        # Tech Club Form
        cursor.execute("""
            INSERT INTO forms (society_id, title, status, published_at)
            VALUES (1, 'Tech Club Recruitment 2024', 'published', %s)
        """, (datetime.now(),))
        tech_form_id = cursor.lastrowid
        
        tech_questions = [
            ("What is your full name?", "text", None, 1),
            ("What is your email address?", "email", None, 1),
            ("Which year are you currently in?", "select", "First Year,Second Year,Third Year,Fourth Year", 1),
            ("What programming languages are you proficient in?", "textarea", None, 1),
            ("Have you worked on any projects? If yes, please describe.", "textarea", None, 1),
            ("Why do you want to join the Tech Club?", "textarea", None, 1),
            ("Are you interested in any specific domain? (AI/ML, Web Dev, App Dev, etc.)", "textarea", None, 0),
        ]
        
        for q_text, q_type, options, is_req in tech_questions:
            cursor.execute("""
                INSERT INTO form_questions (form_id, question_text, question_type, options, is_required, order_index)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tech_form_id, q_text, q_type, options, is_req, tech_questions.index((q_text, q_type, options, is_req))))
        
        print(f"✓ Created Tech Club form (ID: {tech_form_id}) with {len(tech_questions)} questions")
        
        # Drama Society Form
        cursor.execute("""
            INSERT INTO forms (society_id, title, status, published_at)
            VALUES (2, 'Drama Society Auditions 2024', 'published', %s)
        """, (datetime.now(),))
        drama_form_id = cursor.lastrowid
        
        drama_questions = [
            ("What is your full name?", "text", None, 1),
            ("Contact number", "tel", None, 1),
            ("Email address", "email", None, 1),
            ("Have you acted in any plays before? If yes, please list them.", "textarea", None, 0),
            ("What type of roles interest you?", "select", "Lead Actor,Supporting Actor,Comedy,Villain,Character Actor,Any Role", 1),
            ("Do you have experience in scriptwriting or direction?", "textarea", None, 0),
            ("Why do you want to join the Drama Society?", "textarea", None, 1),
            ("Are you comfortable with public speaking and performing?", "select", "Yes,No,Willing to learn", 1),
        ]
        
        for q_text, q_type, options, is_req in drama_questions:
            cursor.execute("""
                INSERT INTO form_questions (form_id, question_text, question_type, options, is_required, order_index)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (drama_form_id, q_text, q_type, options, is_req, drama_questions.index((q_text, q_type, options, is_req))))
        
        print(f"✓ Created Drama Society form (ID: {drama_form_id}) with {len(drama_questions)} questions")
        
        # Table Tennis Society Form
        cursor.execute("""
            INSERT INTO forms (society_id, title, status, published_at)
            VALUES (3, 'Table Tennis Society Recruitment 2024', 'published', %s)
        """, (datetime.now(),))
        tt_form_id = cursor.lastrowid
        
        tt_questions = [
            ("What is your full name?", "text", None, 1),
            ("Email address", "email", None, 1),
            ("Contact number", "tel", None, 1),
            ("Current year of study", "select", "First Year,Second Year,Third Year,Fourth Year", 1),
            ("How long have you been playing table tennis?", "select", "Less than 1 year,1-3 years,3-5 years,5+ years,Never played", 1),
            ("Have you participated in any table tennis tournaments?", "textarea", None, 0),
            ("What is your playing style?", "select", "Offensive,Defensive,All-round,Still learning", 0),
            ("Why do you want to join the Table Tennis Society?", "textarea", None, 1),
            ("Can you commit to regular practice sessions (3 times a week)?", "select", "Yes,Maybe,No", 1),
        ]
        
        for q_text, q_type, options, is_req in tt_questions:
            cursor.execute("""
                INSERT INTO form_questions (form_id, question_text, question_type, options, is_required, order_index)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tt_form_id, q_text, q_type, options, is_req, tt_questions.index((q_text, q_type, options, is_req))))
        
        print(f"✓ Created Table Tennis Society form (ID: {tt_form_id}) with {len(tt_questions)} questions")
        
        connection.commit()
        print("\n✅ Forms seeding completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Seeding recruitment forms with questions...")
    print("=" * 60)
    seed_forms()
