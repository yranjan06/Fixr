from flask import Flask
from flask_login import login_required
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role
import os

# File upload settings
INSTANCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
UPLOAD_FOLDER = os.path.join(INSTANCE_PATH, 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

def create_app():
    # Create instance and uploads folders
    os.makedirs(INSTANCE_PATH, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    app = Flask(__name__, 
                template_folder='frontend', 
                static_folder='frontend', 
                static_url_path='',
                instance_path=INSTANCE_PATH)
    
    app.config.from_object(LocalDevelopmentConfig)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
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
        
        import backend.create_initial_data
        import backend.routes
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
