from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
IST = timezone('Asia/Kolkata')
db = SQLAlchemy()





class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    pincode = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.Integer, nullable=False, default=1234567890)
    role = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False, default='normal')
    is_approved = db.Column(db.Boolean, default=True)
    is_blocked = db.Column(db.Boolean, default=False)
    saved_packs = db.Column(db.String(20), nullable=True)

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False) #emergency, platinum, normal

class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(150), nullable=False)
    p_email = db.Column(db.String(150), nullable=False)
    p_phone = db.Column(db.Integer, nullable=False)
    paddress = db.Column(db.String(300), nullable=False)
    ppassword = db.Column(db.String(150), nullable=False)
    p_pincode = db.Column(db.Integer, nullable=False)
    document_proof = db.Column(db.String(550), nullable=False) 
    experience_years = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    base_price = db.Column(db.Float, nullable=False, default=0.0)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=True)    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
   
    #relationship 
    user = db.relationship('User', backref='professional_profile')
    service = db.relationship('Service', backref=db.backref('professionals', lazy='dynamic'))

class ServicePackage(db.Model):
    __tablename__ = 'service_package'
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.String, nullable=False, default='00:20:00')
    is_flagged = db.Column(db.Boolean, default=False)

    #relationship 
    professional = db.relationship('Professional', backref='service_packages')
    service = db.relationship('Service', backref='service_packages')

class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('service_package.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, nullable=False, default=datetime.now(IST))
    date_of_completion = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='requested') #requested, accepted, completed, closed
    remarks = db.Column(db.String(500))

    # relationship
    customer = db.relationship('User', foreign_keys=[customer_id], backref=db.backref('service_requests', lazy='dynamic'))
    professional = db.relationship('Professional', foreign_keys=[professional_id], backref=db.backref('service_requests', lazy='dynamic'))
  
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(IST))

    #relationship 
    service_request = db.relationship('ServiceRequest', backref='review')
    