from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.services import UserService
from flask import Blueprint
user_app = Blueprint('user_app', __name__)


@user_app.route('/login', methods=['POST'])
def login():
    auth = request.json
    username = auth.get('username')
    password = auth.get('password')
    user = UserService.get_by_username(username)
    if user:
        password_check = UserService.verify_password(username, password)
        if password_check:
            access_token = create_access_token(identity=user.to_json())
            return jsonify(access_token=access_token), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@user_app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
