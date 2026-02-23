from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify


jwt = JWTManager()

# decorators for role-based access control

def admin_required(fn):
   

    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'msg': 'Admins only!'}, 403
        return fn(*args, **kwargs)
    
    return wrapper


def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'student':
            return {'msg': 'Students only!'}, 403
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