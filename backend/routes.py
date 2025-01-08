from flask import current_app as app, jsonify, request, render_template
from flask_security import verify_password, hash_password

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
            'id': user.id
        })
    
    return jsonify({'message': 'Invalid password'}), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')
    
    if not email or not password:
        return jsonify({"message": "Invalid inputs"}), 400
    
    if app.security.datastore.find_user(email=email):
        return jsonify({"message": "User already exists"}), 400
    
    try:
        app.security.datastore.create_user(
            email=email,
            password=hash_password(password),
            roles=[role]
        )
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user"}), 400