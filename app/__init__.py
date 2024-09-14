# app/__init__.py

from flask import Flask
from app.models.user import db
from app.routes.user_routes import user_routes
from app.routes.event_routes import event_routes
from app.routes.admin_event_routes import admin_event_routes
from app.config import Config
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the database
    db.init_app(app)
     
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_routes.login_page'  # Redirect if not logged in

    # Load the user by ID
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(user_routes)
    app.register_blueprint(event_routes)
    app.register_blueprint(admin_event_routes)
    
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app
