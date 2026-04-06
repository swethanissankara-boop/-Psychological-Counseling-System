import os
from flask import Flask
from dotenv import load_dotenv

# Import our setup tools
from extensions import db, login_manager, csrf
from models import User

# Import our Blueprints
from routes.main import main_bp
from routes.admin import admin_bp
from routes.jp import jp_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psych.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register the routes to the app
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(jp_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)