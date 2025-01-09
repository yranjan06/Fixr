from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)
    
    # Two-factor authentication
    tf_phone_number = db.Column(db.String(128))
    tf_primary_method = db.Column(db.String(64))
    tf_totp_secret = db.Column(db.String(255))
    
    # User profile
    user_type = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(500))
    pin_code = db.Column(db.String(10))
    
    # Professional-specific fields
    service_type = db.Column(db.String(50))
    experience_years = db.Column(db.Integer)
    certifications = db.Column(db.String(255))
    
    # Relationships
    roles = db.relationship('Role', secondary='user_roles', 
                          backref=db.backref('users', lazy='dynamic'))
    
    @validates('email')
    def validate_email(self, key, address):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError('Invalid email address')
        return address
    
    @validates('pin_code')
    def validate_pin_code(self, key, pin):
        if pin and (not pin.isdigit() or len(pin) not in [5, 6]):
            raise ValueError('Pin code must be 5 or 6 digits')
        return pin
    
    @validates('experience_years')
    def validate_experience(self, key, years):
        if years is not None and (years < 0 or years > 100):
            raise ValueError('Experience years must be between 0 and 100')
        return years

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
