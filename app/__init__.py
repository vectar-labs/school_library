from flask import Flask, app, config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.models import db
from app.config import Config
from app.auth import jwt


# Import blueprints
from .routes.student import student_bp
from .routes.admin import admin_bp

def create_app(config_name= "default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # extenstions initialization
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # create database tables
    with app.app_context():
        db.create_all()
        
    # create a default admin user if not exists
    from app.models import User
    from werkzeug.security import generate_password_hash
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password=generate_password_hash('101admin101'), role='admin')
            db.session.add(admin_user)
            db.session.commit()
            
    @app.route('/')
    def index():
        return "Welcome to the Student Management System API!"
    
    return app

