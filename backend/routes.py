from flask import current_app as app, jsonify, request, render_template, send_from_directory
from flask_security import verify_password, hash_password, auth_required, current_user
from werkzeug.utils import secure_filename
from backend.models import db, User
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def serve_vue_app():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"message": "Missing email or password"}), 400

        user = app.security.datastore.find_user(email=data['email'])
        if not user or not verify_password(data['password'], user.password):
            return jsonify({"message": "Invalid credentials"}), 401

        if not user.active:
            return jsonify({"message": "Account is deactivated"}), 403

        return jsonify({
            'token': user.get_auth_token(),
            'email': user.email,
            'role': user.roles[0].name if user.roles else None,
            'user_type': user.user_type,
            'id': user.id
        })

    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({"message": "Server error"}), 500

@app.route('/register/customer', methods=['POST'])
def register_customer():
    try:
        data = request.get_json()
        required_fields = ['email', 'password', 'full_name']
        
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        if app.security.datastore.find_user(email=data['email']):
            return jsonify({"message": "Email already registered"}), 409

        user = app.security.datastore.create_user(
            email=data['email'],
            password=hash_password(data['password']),
            full_name=data['full_name'],
            address=data.get('address'),
            pin_code=data.get('pin_code'),
            user_type='customer',
            roles=['customer']
        )
        
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Customer registration error: {str(e)}")
        return jsonify({"message": "Registration failed"}), 500

@app.route('/register/professional', methods=['POST'])
def register_professional():
    try:
        if 'certifications' not in request.files:
            return jsonify({"message": "No certification file provided"}), 400

        file = request.files['certifications']
        if not file or not allowed_file(file.filename):
            return jsonify({"message": "Invalid file type"}), 400

        required_fields = ['email', 'password', 'full_name', 'service_type']
        if not all(field in request.form for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        if app.security.datastore.find_user(email=request.form['email']):
            return jsonify({"message": "Email already registered"}), 409

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        user = app.security.datastore.create_user(
            email=request.form['email'],
            password=hash_password(request.form['password']),
            full_name=request.form['full_name'],
            service_type=request.form['service_type'],
            experience_years=int(request.form.get('experience_years', 0)),
            address=request.form.get('address'),
            pin_code=request.form.get('pin_code'),
            certifications=filepath,
            user_type='professional',
            roles=['professional']
        )
        
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Professional registration error: {str(e)}")
        return jsonify({"message": "Registration failed"}), 500