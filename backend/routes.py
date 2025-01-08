from flask import current_app as app, jsonify, request, render_template
from flask_security import verify_password, hash_password
from werkzeug.utils import secure_filename
from backend.models import db
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Invalid inputs"}), 400

    user = app.security.datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if verify_password(password, user.password):
        return jsonify({
            'token': user.get_auth_token(),
            'email': user.email,
            'role': user.roles[0].name,
            'user_type': user.user_type,
            'id': user.id
        })

    return jsonify({'message': 'Invalid password'}), 400

@app.route('/register/customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    address = data.get('address')
    pin_code = data.get('pin_code')

    if not email or not password or not full_name:
        return jsonify({"message": "Invalid inputs"}), 400

    if app.security.datastore.find_user(email=email):
        return jsonify({"message": "User already exists"}), 400

    try:
        app.security.datastore.create_user(
            email=email,
            password=hash_password(password),
            full_name=full_name,
            address=address,
            pin_code=pin_code,
            user_type='customer',
            roles=['customer']
        )
        db.session.commit()
        return jsonify({"message": "Customer created successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating customer"}), 400

@app.route('/register/professional', methods=['POST'])
def register_professional():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    service_type = data.get('service_type')
    experience_years = data.get('experience_years')
    address = data.get('address')
    pin_code = data.get('pin_code')

    if not email or not password or not full_name or not service_type:
        return jsonify({"message": "Invalid inputs"}), 400

    if app.security.datastore.find_user(email=email):
        return jsonify({"message": "User already exists"}), 400

    certifications_file = request.files.get('certifications')
    certifications_path = None

    if certifications_file and allowed_file(certifications_file.filename):
        filename = secure_filename(certifications_file.filename)
        certifications_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        certifications_file.save(certifications_path)

    try:
        app.security.datastore.create_user(
            email=email,
            password=hash_password(password),
            full_name=full_name,
            service_type=service_type,
            experience_years=int(experience_years) if experience_years else None,
            address=address,
            pin_code=pin_code,
            certifications=certifications_path,
            user_type='professional',
            roles=['professional']
        )
        db.session.commit()
        return jsonify({"message": "Professional created successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating professional"}), 400