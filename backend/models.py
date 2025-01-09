from datetime import datetime
from pytz import timezone
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

IST = timezone("Asia/Kolkata")
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    address = db.Column(db.String(300))
    pincode = db.Column(db.Integer)
    phone = db.Column(db.String(15), nullable=False, default="1234567890")
    is_approved = db.Column(db.Boolean, default=True)
    is_blocked = db.Column(db.Boolean, default=False)


class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False)


class Professional(db.Model):
    __tablename__ = "professional"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    document_proof = db.Column(db.String(500), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    service = db.relationship("Service", backref="professionals")


class ServicePackage(db.Model):
    __tablename__ = "service_package"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.String, nullable=False, default="00:20:00")
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"))
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    professional = db.relationship("Professional", backref="packages")
    service = db.relationship("Service", backref="packages")


class ServiceRequest(db.Model):
    __tablename__ = "service_request"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"))
    package_id = db.Column(db.Integer, db.ForeignKey("service_package.id"), nullable=False)
    date_of_request = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(IST))
    status = db.Column(db.String(20), default="requested")


class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey("service_request.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(IST))
