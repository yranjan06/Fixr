from flask import Flask
from flask_login import login_required
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role
import os

# File upload settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
UPLOAD_FOLDER = os.path.join(INSTANCE_PATH, 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

def create_app():
    # Create instance and uploads folders with proper permissions
    os.makedirs(INSTANCE_PATH, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Ensure proper permissions for SQLite database directory
    os.chmod(INSTANCE_PATH, 0o755)
    
    app = Flask(__name__, 
                template_folder='frontend', 
                static_folder='frontend', 
                static_url_path='',
                instance_path=INSTANCE_PATH)
    
    app.config.from_object(LocalDevelopmentConfig)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(INSTANCE_PATH, 'database.sqlite3')}"
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Flask-Security setup
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore=datastore)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Import routes after database initialization
        import backend.routes
        
        # Create initial data only if database is empty
        if not User.query.first():
            import backend.create_initial_data
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)