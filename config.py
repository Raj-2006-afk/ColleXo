import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/collexo_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx'}
    APP_NAME = 'ColleXo'
    COLLEGE_NAME = os.getenv('COLLEGE_NAME', 'NSUT')
    SOCIETIES_PER_PAGE = 12
    FORMS_PER_PAGE = 10
    SUBMISSIONS_PER_PAGE = 20

    SOCIETY_CATEGORIES = {
        'technical': 'Technical',
        'cultural': 'Cultural',
        'sports': 'Sports',
        'literary': 'Literary',
        'social_service': 'Social Service',
        'other': 'Other'
    }
