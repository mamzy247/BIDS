#!/usr/bin/env python3
"""
Baze Internship Database System
Main Flask Application
"""

import os
import sqlite3
from flask import Flask, g, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime

# Import configuration
from config import config

# Create Flask app
app = Flask(__name__)

# Load configuration
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# Database connection
def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(error=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize database on first run
def init_db():
    """Initialize the database"""
    with app.app_context():
        db = get_db()
        with app.open_resource('database/schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

# Register teardown handler
app.teardown_appcontext(close_db)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    from models.user import User
    return User.get(user_id)

# Register blueprints
def register_blueprints(app):
    """Register all application blueprints"""
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.hod import hod_bp
    from routes.supervisor import supervisor_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(hod_bp, url_prefix='/hod')
    app.register_blueprint(supervisor_bp, url_prefix='/supervisor')
    app.register_blueprint(admin_bp, url_prefix='/admin')

# Register error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db = get_db()
    db.rollback()
    return render_template('errors/500.html'), 500

# Context processors
@app.context_processor
def inject_globals():
    """Inject global variables into templates"""
    return {
        'university_name': app.config['UNIVERSITY_NAME'],
        'academic_year': app.config['ACADEMIC_YEAR'],
        'current_year': datetime.now().year
    }

# Routes
@app.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        # Redirect based on user type
        if current_user.user_type == 'student':
            return redirect(url_for('student.dashboard'))
        elif current_user.user_type == 'hod':
            return redirect(url_for('hod.dashboard'))
        elif current_user.user_type == 'supervisor':
            return redirect(url_for('supervisor.dashboard'))
        elif current_user.user_type == 'admin':
            return redirect(url_for('admin.dashboard'))
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# CLI commands
@app.cli.command()
def initdb():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')

@app.cli.command()
def create_admin():
    """Create an admin user."""
    from models.user import User
    
    email = input('Admin email: ')
    password = input('Admin password: ')
    full_name = input('Full name: ')
    
    # Check if user exists
    if User.get_by_email(email):
        print('User already exists!')
        return
    
    # Create admin user
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO users (email, password_hash, full_name, user_type) VALUES (?, ?, ?, ?)',
        (email, generate_password_hash(password), full_name, 'admin')
    )
    db.commit()
    print(f'Admin user {email} created successfully!')

# Run the application
if __name__ == '__main__':
    # Register blueprints
    register_blueprints(app)
    
    # Check if database exists, if not initialize it
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if not os.path.exists(db_path):
        print("Database not found. Initializing...")
        with app.app_context():
            init_db()
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )