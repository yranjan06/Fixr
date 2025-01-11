class BaseConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    # SQLite database for development
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev_database.sqlite3"
    
    # Debug mode enabled for development environment
    DEBUG = True
    
    # Password hashing settings
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Secure password hashing using bcrypt
    SECURITY_PASSWORD_SALT = 'a_very_secure_salt_key'
    
    # Application's secret key
    SECRET_KEY = "a_super_secret_development_key"
    
    # Custom header for token-based authentication
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Auth-Token'
    
    # CSRF protection disabled (only for development)
    WTF_CSRF_ENABLED = False
