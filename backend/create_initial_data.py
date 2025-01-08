from flask import current_app as app
from backend.models import db
from flask_security import hash_password

with app.app_context():
    db.create_all()
    
    datastore = app.security.datastore
    
    # Create roles
    datastore.find_or_create_role(name='admin', description='Administrator')
    datastore.find_or_create_role(name='user', description='Regular User')
    
    # Create a test admin user
    if not datastore.find_user(email='admin@test.com'):
        datastore.create_user(
            email='admin@test.com',
            password=hash_password('admin123'),
            roles=['admin']
        )
    
    db.session.commit()
