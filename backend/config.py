import os
from datetime import timedelta

class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings - require environment variables
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = timedelta(days=5)
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    
    # CSRF protection
    WTF_CSRF_ENABLED = True
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/uploads')
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Database settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/database.sqlite3"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    WTF_CSRF_ENABLED = True