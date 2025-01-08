from flask import Flask
from flask_login import login_required
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role
import os

# File upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance/uploads')
ALLOWED_EXTENSIONS = {'pdf'}

def create_app():
    app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='')
    
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
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
        import backend.create_initial_data
        import backend.routes
        
        # Create database tables
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)