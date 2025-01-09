from flask import current_app
from backend.models import db, User, Role
from flask_security import hash_password
import os

def init_db():
    # Create roles if they don't exist
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)
    
    customer_role = Role.query.filter_by(name='customer').first()
    if not customer_role:
        customer_role = Role(name='customer', description='Customer User')
        db.session.add(customer_role)
    
    professional_role = Role.query.filter_by(name='professional').first()
    if not professional_role:
        professional_role = Role(name='professional', description='Service Provider')
        db.session.add(professional_role)
    
    # Create admin user if it doesn't exist
    admin_user = User.query.filter_by(email='admin@test.com').first()
    if not admin_user:
        admin_user = User(
            email='admin@test.com',
            password=hash_password('admin123'),
            active=True,
            fs_uniquifier=os.urandom(16).hex(),
            full_name='Admin User',
            user_type='admin'
        )
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
    
    # Create a test customer if it doesn't exist
    customer_user = User.query.filter_by(email='customer@test.com').first()
    if not customer_user:
        customer_user = User(
            email='customer@test.com',
            password=hash_password('customer123'),
            active=True,
            fs_uniquifier=os.urandom(16).hex(),
            full_name='Test Customer',
            user_type='customer',
            address='123 Test St',
            pin_code='12345'
        )
        customer_user.roles.append(customer_role)
        db.session.add(customer_user)
    
    # Create a test professional if it doesn't exist
    professional_user = User.query.filter_by(email='professional@test.com').first()
    if not professional_user:
        professional_user = User(
            email='professional@test.com',
            password=hash_password('professional123'),
            active=True,
            fs_uniquifier=os.urandom(16).hex(),
            full_name='Test Professional',
            user_type='professional',
            service_type='plumber',
            experience_years=5,
            address='456 Pro St',
            pin_code='67890'
        )
        professional_user.roles.append(professional_role)
        db.session.add(professional_user)
    
    try:
        db.session.commit()
        print("Initial data created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating initial data: {str(e)}")

# This will run when the module is imported
init_db()