import json

from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.services import UserService
from flask import Blueprint
from app.utils.auth_utils import is_staff
from app.utils.json_utils import jsonify_wrapper_mongo_engine

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

@user_app.route('/create-staff-user', methods=['POST'])
@jwt_required()
@is_staff
def create_staff_user():
    data = request.json
    if data.get('is_superuser', False):
        current_user = json.loads(get_jwt_identity())
        is_current_user_superuser = current_user.get('is_superuser', False)
        if not is_current_user_superuser:
            return jsonify({"data": "UnAuthorized"}), 403
    user = UserService.create_user(**data)
    return jsonify_wrapper_mongo_engine(user)

@user_app.route('/create-customer-user', methods=['POST'])
def create_customer_user():
    data = request.json
    data.pop('is_staff', None)
    data.pop('is_superuser', None)
    user = UserService.create_user(**data)
    return jsonify_wrapper_mongo_engine(user)