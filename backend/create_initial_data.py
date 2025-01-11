from flask import current_app as app
from backend.models import db, User, Role, Service
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
    db.create_all()

    # Initialize Flask-Security user data store
    user_datastore: SQLAlchemyUserDatastore = app.security.datastore

    # Create roles
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='provider', description='Service Provider')
    user_datastore.find_or_create_role(name='customer', description='Customer')

    # Create default users
    if not user_datastore.find_user(email='admin@urbancompany.com'):
        user_datastore.create_user(
            email='admin@urbancompany.com',
            password=hash_password('admin123'),
            roles=['admin']
        )

    if not user_datastore.find_user(email='provider01@urbancompany.com'):
        user_datastore.create_user(
            email='provider01@urbancompany.com',
            password=hash_password('provider123'),
            roles=['provider']
        )

    if not user_datastore.find_user(email='customer01@urbancompany.com'):
        user_datastore.create_user(
            email='customer01@urbancompany.com',
            password=hash_password('customer123'),
            roles=['customer']
        )

    # Create sample services
    services = [
        Service(name='Plumbing', base_price=50.0, description='Basic plumbing services.', category='normal'),
        Service(name='Electrical', base_price=60.0, description='Basic electrical repairs.', category='normal'),
        Service(name='Cleaning', base_price=40.0, description='Home cleaning services.', category='platinum'),
        Service(name='Emergency Repair', base_price=100.0, description='24/7 emergency repair services.', category='emergency'),
    ]
    db.session.bulk_save_objects(services)

    db.session.commit()
    print("Initial data created!")
