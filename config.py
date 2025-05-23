import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database', 'baze_internship.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload config
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # Email config
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@baze.edu.ng'
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Pagination
    STUDENTS_PER_PAGE = 20
    LOGS_PER_PAGE = 10
    
    # University specific
    UNIVERSITY_NAME = "Baze University"
    UNIVERSITY_EMAIL_DOMAIN = "@baze.edu.ng"
    ACADEMIC_YEAR = "2024/2025"
    
    # File paths
    WORKFLOW_CHARTS_PATH = os.path.join(UPLOAD_FOLDER, 'workflow_charts')
    WORKSPACE_PHOTOS_PATH = os.path.join(UPLOAD_FOLDER, 'workspace_photos')
    DOCUMENTS_PATH = os.path.join(UPLOAD_FOLDER, 'documents')
    
    @staticmethod
    def init_app(app):
        # Create upload directories if they don't exist
        os.makedirs(Config.WORKFLOW_CHARTS_PATH, exist_ok=True)
        os.makedirs(Config.WORKSPACE_PHOTOS_PATH, exist_ok=True)
        os.makedirs(Config.DOCUMENTS_PATH, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Override with production-specific settings
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}