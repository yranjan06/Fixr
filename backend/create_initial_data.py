from flask import current_app as app
from backend.models import db
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore : SQLAlchemyUserDatastore = app.security.datastore

    userdatastore.find_or_create_role(name = 'admin', description = 'superuser')
    userdatastore.find_or_create_role(name = 'user', description = 'general user')
    userdatastore.find_or_create_role(name = 'professional', description = 'service provider')

    if (not userdatastore.find_user(email = 'admin@study.iitm.ac.in')):
        userdatastore.create_user(email = 'admin@study.iitm.ac.in', password = hash_password('pass'), roles = ['admin'] )
    if (not userdatastore.find_user(email = 'user01@study.iitm.ac.in')):
        userdatastore.create_user(email = 'user01@study.iitm.ac.in', password = hash_password('pass'), roles = ['user'] ) # for testing

    if (not userdatastore.find_user(email = 'professional01@study.iitm.ac.in')):
        userdatastore.create_user(email = 'professional01@study.iitm.ac.in', password = hash_password('pass'), roles = ['professional'] ) # for testing

    db.session.commit()