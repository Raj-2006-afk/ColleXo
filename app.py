from flask import Flask, render_template, session
from config import Config
from models import db
from blueprints.auth import auth_bp
from blueprints.societies import societies_bp
from blueprints.students import students_bp
from blueprints.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(societies_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        return {
            'app_name': Config.APP_NAME,
            'college_name': Config.COLLEGE_NAME,
            'current_user_id': session.get('user_id'),
            'current_user_role': session.get('user_role'),
            'categories': Config.SOCIETY_CATEGORIES
        }

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.route('/')
    def index():
        from models import Society
        categories = Config.SOCIETY_CATEGORIES
        category_counts = {}
        for cat_value, cat_name in categories.items():
            count = Society.query.filter_by(category=cat_value, is_approved=True, is_active=True).count()
            category_counts[cat_value] = {'name': cat_name, 'count': count}
        featured_societies = Society.query.filter_by(
            is_approved=True, is_active=True
        ).order_by(Society.views_count.desc()).limit(6).all()
        return render_template('index.html',
                             category_counts=category_counts,
                             categories=categories,
                             featured_societies=featured_societies)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
