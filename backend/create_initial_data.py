from flask import current_app as app
from backend.models import db
from flask_security import hash_password
import os

def init_db():
    with app.app_context():
        # Ensure database directory exists
        os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')), exist_ok=True)
        
        db.create_all()

        datastore = app.security.datastore

        # Create roles
        datastore.find_or_create_role(name='admin', description='Administrator')
        datastore.find_or_create_role(name='customer', description='Customer User')
        datastore.find_or_create_role(name='professional', description='Service Provider')

        # Create a test admin user if it doesn't exist
        if not datastore.find_user(email='admin@test.com'):
            datastore.create_user(
                email='admin@test.com',
                password=hash_password('admin123'),
                roles=['admin']
            )

        db.session.commit()

# Call init_db if this file is run directly
if __name__ == '__main__':
    init_db()