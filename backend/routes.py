from flask import current_app as app, jsonify, request, render_template, send_from_directory
from flask_security import verify_password, hash_password, auth_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .models import db, User
from .schemas import CustomerSchema, ProfessionalSchema
from .utils import validate_file
from .errors import APIError
import os

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/')
def serve_vue_app():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    try:
        data = request.get_json()
        if not data:
            raise APIError("No data provided", 400)

        user = app.security.datastore.find_user(email=data.get('email'))
        if not user or not verify_password(data.get('password', ''), user.password):
            raise APIError("Invalid credentials", 401)

        if not user.active:
            raise APIError("Account is deactivated", 403)

        # Update login stats
        user.last_login_at = user.current_login_at
        user.current_login_at = datetime.utcnow()
        user.last_login_ip = user.current_login_ip
        user.current_login_ip = request.remote_addr
        user.login_count = (user.login_count or 0) + 1
        db.session.commit()

        return jsonify({
            'token': user.get_auth_token(),
            'email': user.email,
            'role': user.roles[0].name if user.roles else None,
            'user_type': user.user_type,
            'id': user.id
        })

    except APIError as e:
        raise e
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        raise APIError("Server error", 500)

@app.route('/register/customer', methods=['POST'])
@limiter.limit("3 per hour")
def register_customer():
    try:
        data = request.get_json()
        if not data:
            raise APIError("No data provided", 400)

        # Validate input data
        errors = CustomerSchema().validate(data)
        if errors:
            raise APIError(f"Validation error: {errors}", 400)

        if app.security.datastore.find_user(email=data['email']):
            raise APIError("Email already registered", 409)

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

    except APIError as e:
        raise e
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Customer registration error: {str(e)}")
        raise APIError("Registration failed", 500)

@app.route('/register/professional', methods=['POST'])
@limiter.limit("3 per hour")
def register_professional():
    try:
        if 'certifications' not in request.files:
            raise APIError("No certification file provided", 400)

        # Validate file
        file = request.files['certifications']
        try:
            filename = validate_file(file)
        except ValueError as e:
            raise APIError(str(e), 400)

        # Validate form data
        form_data = request.form.to_dict()
        errors = ProfessionalSchema().validate(form_data)
        if errors:
            raise APIError(f"Validation error: {errors}", 400)

        if app.security.datastore.find_user(email=form_data['email']):
            raise APIError("Email already registered", 409)

        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        user = app.security.datastore.create_user(
            email=form_data['email'],
            password=hash_password(form_data['password']),
            full_name=form_data['full_name'],
            service_type=form_data['service_type'],
            experience_years=int(form_data.get('experience_years', 0)),
            address=form_data.get('address'),
            pin_code=form_data.get('pin_code'),
            certifications=filepath,
            user_type='professional',
            roles=['professional']
        )
        
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201

    except APIError as e:
        raise e
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Professional registration error: {str(e)}")
        raise APIError("Registration failed", 500)