from flask import Blueprint, request, jsonify
from models.user_model import create_user, get_user_by_phone
from utils.auth import hash_password, check_password

auth_bp = Blueprint('auth', __name__)

# =========================
# REGISTER
# =========================
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    name = data.get('name')
    phone = data.get('phone')
    password = data.get('password')
    flat_no = data.get('flat_no')
    role = data.get('role', 'user')
    building_id = data.get('building_id')

    # check existing user
    existing_user = get_user_by_phone(phone)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # hash password
    hashed_password = hash_password(password)

    # save user
    create_user(name, phone, hashed_password, flat_no, role, building_id)

    return jsonify({"message": "User registered successfully"}), 201


# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    phone = data.get('phone')
    password = data.get('password')

    user = get_user_by_phone(phone)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if check_password(password, user['password']):
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user['user_id'],
                "name": user['name'],
                "role": user['role']
            }
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401