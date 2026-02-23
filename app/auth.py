from flask_jwt_extended import JWTManager, get_jwt_identity
from functools import wraps
from flask import jsonify

jwt = JWTManager()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from app.models import Admin  # Import here to avoid circular import
        current_user_id = get_jwt_identity()
        admin = Admin.query.get(current_user_id)
        if not admin:
            return jsonify({'msg': 'Admins only!'}), 403
        return fn(*args, **kwargs)
    return wrapper

def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from app.models import Student  # Import here to avoid circular import
        current_user_id = get_jwt_identity()
        student = Student.query.get(current_user_id)
        if not student:
            return jsonify({'msg': 'Students only!'}), 403
        return fn(*args, **kwargs)
    return wrapper

# JWT error handlers

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({'msg': 'Missing Authorization Header'}), 401

@jwt.invalid_token_loader
def invalid_token_response(callback):
    return jsonify({'msg': 'Invalid token'}), 422

@jwt.expired_token_loader
def expired_token_response(callback):
    return jsonify({'msg': 'Token has expired'}), 401