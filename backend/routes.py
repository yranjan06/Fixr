from flask import render_template, jsonify, request
from flask_security import auth_required, verify_password, hash_password
from backend.models import db
from flask import current_app as app

datastore = app.security.datastore

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

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if verify_password(password, user.password):
        return jsonify({
            'token': user.get_auth_token(),
            'email': user.email,
            'roles': [role.name for role in user.roles],
            'id': user.id
        }), 200

    return jsonify({"message": "Incorrect password"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or role not in ['admin', 'provider', 'customer']:
        return jsonify({"message": "Invalid inputs"}), 400

    if datastore.find_user(email=email):
        return jsonify({"message": "User already exists"}), 400

    try:
        datastore.create_user(email=email, password=hash_password(password), roles=[role], active=True)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating user: {str(e)}"}), 500
