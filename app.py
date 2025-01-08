from flask import Flask
from flask_login import login_required
from flask_security import Security, SQLAlchemyUserDatastore
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role

# File upload settings
UPLOAD_FOLDER = 'instance/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def create_app():
    app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='/static')
    app.config.from_object(LocalDevelopmentConfig)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize database
    db.init_app(app)

    # Flask-Security setup
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore=datastore, register_blueprint=False)

    app.app_context().push()
    return app

app = create_app()

import backend.create_initial_data
import backend.routes

if __name__ == '__main__':
    app.run(debug=True)