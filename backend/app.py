from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.db import init_database
from routes.auth_routes import auth_bp
from routes.society_routes import society_bp
from routes.form_routes import form_bp
from routes.application_routes import application_bp
from routes.admin_routes import admin_bp

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours

# Initialize extensions
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Initialize database (creates DB, tables, and seeds data if needed)
init_database()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(society_bp, url_prefix='/api/societies')
app.register_blueprint(form_bp, url_prefix='/api/forms')
app.register_blueprint(application_bp, url_prefix='/api/applications')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Root route
@app.route('/')
def index():
    return '''
    <h1>ColleXo - College Societies Management System</h1>
    <p>Backend API is running!</p>
    <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Register</a></li>
        <li><a href="/api/societies/browse">Browse Societies (API)</a></li>
    </ul>
    '''

# Frontend routes
from flask import render_template

@app.route('/login')
def login_page():
    return render_template('auth/login.html')

@app.route('/register')
def register_page():
    return render_template('auth/register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/student/dashboard')
def student_dashboard():
    return render_template('student/dashboard.html')

@app.route('/society/dashboard')
def society_dashboard():
    return render_template('society/dashboard.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ColleXo Backend Starting...")
    print("=" * 60)
    print("📍 Server: http://localhost:5000")
    print("📊 Database: MySQL (localhost:3306)")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
