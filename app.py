from flask import Flask
from flask_login import login_required
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend.config import LocalDevelopmentConfig, ProductionConfig
from backend.models import db, User, Role
from backend.errors import register_error_handlers
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import timedelta

# File upload settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
UPLOAD_FOLDER = os.path.join(INSTANCE_PATH, 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
LOG_FOLDER = os.path.join(INSTANCE_PATH, 'logs')

def setup_logging(app):
    """Configure application logging"""
    os.makedirs(LOG_FOLDER, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        os.path.join(LOG_FOLDER, 'fixr.log'),
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Fixr startup')

def create_app(config_class=None):
    """Application factory function"""
    try:
        # Create required directories with proper permissions
        for path in [INSTANCE_PATH, UPLOAD_FOLDER, LOG_FOLDER]:
            os.makedirs(path, exist_ok=True)
            os.chmod(path, 0o750)  # More restrictive permissions
        
        app = Flask(__name__, 
                   template_folder='frontend', 
                   static_folder='frontend', 
                   static_url_path='',
                   instance_path=INSTANCE_PATH)
        
        # Determine configuration
        if config_class is None:
            config_class = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else LocalDevelopmentConfig
        
        app.config.from_object(config_class)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
        
        # Ensure required environment variables are set
        required_env_vars = [
            'SECRET_KEY', 
            'SECURITY_PASSWORD_SALT',
            'DATABASE_URL',
            'REDIS_URL'
        ]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Initialize extensions
        db.init_app(app)
        
        # Setup CORS with more restrictive settings
        CORS(app, resources={
            r"/*": {
                "origins": app.config.get('ALLOWED_ORIGINS', []),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Authentication-Token"],
                "expose_headers": ["Content-Type", "X-CSRFToken"],
                "supports_credentials": True,
                "max_age": 600
            }
        })
        
        # Initialize rate limiter with Redis
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"],
            storage_uri=os.getenv('REDIS_URL')
        )
        
        # Setup Flask-Security with enhanced settings
        datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security(app, datastore=datastore)
        
        # Register error handlers
        register_error_handlers(app)
        
        # Setup logging
        setup_logging(app)
        
        # Security headers middleware
        @app.after_request
        def add_security_headers(response):
            response.headers.update({
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
                'Content-Security-Policy': "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; img-src 'self' data:;",
                'Referrer-Policy': 'strict-origin-when-cross-origin',
                'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
            })
            return response
        
        with app.app_context():
            db.create_all()
            import backend.routes
            
            # Create initial data only if database is empty
            if not User.query.first():
                try:
                    import backend.create_initial_data
                    app.logger.info('Initial data created successfully')
                except Exception as e:
                    app.logger.error(f'Error creating initial data: {str(e)}')
        
        return app
    
    except Exception as e:
        print(f"Failed to create application: {str(e)}")
        raise

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)