class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Enhanced security settings
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
    SECURITY_PASSWORD_HASH = 'argon2'
    SECURITY_PASSWORD_LENGTH_MIN = 12
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = timedelta(days=1)
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_TWO_FACTOR = True
    SECURITY_TWO_FACTOR_RESCUE_MAIL = True
    
    # Session security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # File upload settings
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/uploads')
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ['REDIS_URL']
    RATELIMIT_STRATEGY = "fixed-window-elastic-expiry"
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    
    # Database settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 15,
        'pool_size': 30
    }
    
    # CORS settings
    ALLOWED_ORIGINS = ['https://yourdomain.com']  # Update with your domain

class DevelopmentConfig(Config):
    DEBUG = True
    ALLOWED_ORIGINS = ['http://localhost:5000']
    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/database.sqlite3"
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']