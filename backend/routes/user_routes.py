import bcrypt
from flask import Blueprint, request, jsonify
from models import db, Users

users_bp = Blueprint('users', __name__)

# Signup route
@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Save the user with the hashed password
    new_user = Users(
        full_name=data['full_name'],
        email=data['email'],
        password=hashed_password.decode('utf-8'),  # Store the hashed password as a string
        team_name=data['team_name'],
        ts=data['ts']
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# Login route
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(email=data['email']).first()

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"message": "Login successful!", "user": {"id": user.id, "full_name": user.full_name, "loggedInStatus": True}}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
