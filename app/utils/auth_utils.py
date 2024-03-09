from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
import json

# Custom decorator to check if user is authenticated
def is_authenticated(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_user = json.loads(get_jwt_identity())
        if current_user is None:
            return jsonify({'error': 'Authentication required'}), 401
        return func(*args, **kwargs)
    return decorated_function

# Custom decorator to check if user is staff
def is_staff(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_user = json.loads(get_jwt_identity())
        if not current_user or not current_user.get('is_staff', False):
            return jsonify({'error': 'Only staff users can access this resource'}), 403
        return func(*args, **kwargs)
    return decorated_function

# Custom decorator to check if user is superuser
def is_superuser(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_user = json.loads(get_jwt_identity())
        if not current_user or not current_user.get('is_superuser', False):
            return jsonify({'error': 'Only superusers can access this resource'}), 403
        return func(*args, **kwargs)
    return decorated_function
