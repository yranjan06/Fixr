import os
from datetime import timedelta

class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'your-salt-here')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = timedelta(days=5)
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

class LocalDevelopmentConfig(Config):
    DEBUG = True
    # Database URI will be set in app.py
    WTF_CSRF_ENABLED = False  # Only for development