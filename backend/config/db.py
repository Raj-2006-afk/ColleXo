import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime, timedelta

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}

DB_NAME = 'collexo'

def get_connection(include_db=True):
    """Get MySQL connection with dictionary cursor"""
    try:
        config = DB_CONFIG.copy()
        if include_db:
            config['database'] = DB_NAME
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    """Initialize database, tables, and seed data"""
    print("\n🔧 Initializing Database...")
    
    # Step 1: Create database if not exists
    connection = get_connection(include_db=False)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"✅ Database '{DB_NAME}' ready")
            connection.commit()
        except Error as e:
            print(f"❌ Error creating database: {e}")
        finally:
            cursor.close()
            connection.close()
    
    # Step 2: Create tables
    create_tables()
    
    # Step 3: Seed initial data
    seed_data()
    
    print("✅ Database initialization complete!\n")

def create_tables():
    """Create all required tables in correct order (respecting foreign keys)"""
    connection = get_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Set MySQL engine to InnoDB for foreign key support
        cursor.execute("SET default_storage_engine=InnoDB")
        
        # Create users table first (no dependencies)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(255) NOT NULL,
                user_email VARCHAR(255) UNIQUE NOT NULL,
                user_password VARCHAR(255) NOT NULL,
                user_role ENUM('student', 'societyHead', 'admin') NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print(f"✅ Table 'users' ready")
        
        # Create societies table (depends on users)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS societies (
                society_id INT AUTO_INCREMENT PRIMARY KEY,
                society_name VARCHAR(255) UNIQUE NOT NULL,
                tagline VARCHAR(500),
                description TEXT,
                category VARCHAR(100),
                logo_url VARCHAR(500),
                member_count INT DEFAULT 0,
                admission_open BOOLEAN DEFAULT TRUE,
                admission_deadline DATE,
                society_head_id INT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (society_head_id) REFERENCES users(user_id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print(f"✅ Table 'societies' ready")
        
        # Create forms table (depends on societies)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forms (
                form_id INT AUTO_INCREMENT PRIMARY KEY,
                society_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                status ENUM('draft', 'published') DEFAULT 'draft',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                published_at DATETIME NULL,
                FOREIGN KEY (society_id) REFERENCES societies(society_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print(f"✅ Table 'forms' ready")
        
        # Create applications table (depends on users, societies, and forms)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                application_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                society_id INT NOT NULL,
                form_id INT NOT NULL,
                application_date DATE NOT NULL,
                status ENUM('pending', 'shortlisted', 'accepted', 'rejected') DEFAULT 'pending',
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (society_id) REFERENCES societies(society_id) ON DELETE CASCADE,
                FOREIGN KEY (form_id) REFERENCES forms(form_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print(f"✅ Table 'applications' ready")
        
        connection.commit()
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def seed_data():
    """Insert initial data if tables are empty"""
    connection = get_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count > 0:
            print("ℹ️  Seed data already exists, skipping...")
            return
        
        print("📝 Seeding initial data...")
        
        # Hash passwords
        admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        head1_password = bcrypt.hashpw('head123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        head2_password = bcrypt.hashpw('head123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        student_password = bcrypt.hashpw('student123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insert admin user
        cursor.execute("""
            INSERT INTO users (user_name, user_email, user_password, user_role)
            VALUES (%s, %s, %s, %s)
        """, ('Admin User', 'admin@collexo.com', admin_password, 'admin'))
        
        # Insert society heads
        cursor.execute("""
            INSERT INTO users (user_name, user_email, user_password, user_role)
            VALUES (%s, %s, %s, %s)
        """, ('John Doe', 'john@collexo.com', head1_password, 'societyHead'))
        society_head_1_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO users (user_name, user_email, user_password, user_role)
            VALUES (%s, %s, %s, %s)
        """, ('Jane Smith', 'jane@collexo.com', head2_password, 'societyHead'))
        society_head_2_id = cursor.lastrowid
        
        # Insert sample student
        cursor.execute("""
            INSERT INTO users (user_name, user_email, user_password, user_role)
            VALUES (%s, %s, %s, %s)
        """, ('Test Student', 'student@collexo.com', student_password, 'student'))
        
        print("  ✅ Created 4 users (1 admin, 2 society heads, 1 student)")
        
        # Insert sample societies
        deadline_1 = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        deadline_2 = (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d')
        
        cursor.execute("""
            INSERT INTO societies (society_name, tagline, description, category, logo_url, 
                                   member_count, admission_open, admission_deadline, society_head_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('Tech Club', 'Innovate. Build. Learn.',
              'A community of technology enthusiasts who build innovative projects and learn together.',
              'Technical', '/static/images/tech-club.png', 45, True, deadline_1, society_head_1_id))
        tech_club_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO societies (society_name, tagline, description, category, logo_url,
                                   member_count, admission_open, admission_deadline, society_head_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('Drama Society', 'Express. Perform. Inspire.',
              'Bringing stories to life through theater, acting, and creative expression.',
              'Cultural', '/static/images/drama-society.png', 32, True, deadline_2, society_head_2_id))
        drama_society_id = cursor.lastrowid
        
        print("  ✅ Created 2 societies")
        
        # Insert sample recruitment form
        cursor.execute("""
            INSERT INTO forms (society_id, title, status, published_at)
            VALUES (%s, %s, %s, %s)
        """, (tech_club_id, 'Tech Club Recruitment 2025', 'published', datetime.now()))
        
        print("  ✅ Created 1 recruitment form")
        
        connection.commit()
        print("✅ Seed data inserted successfully!")
        
    except Error as e:
        print(f"❌ Error seeding data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
