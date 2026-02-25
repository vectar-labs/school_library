from flask_jwt_extended import JWTManager, get_jwt_identity, get_jwt
from functools import wraps
from flask import jsonify

jwt = JWTManager()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # First check if token is valid (jwt_required should be called before this)
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'msg': 'Invalid token'}), 401
        
        # Check role claim
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'msg': 'Admins only!'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'msg': 'Invalid token'}), 401
            
        claims = get_jwt()
        if claims.get('role') != 'student':
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
def expired_token_response(jwt_header, jwt_payload):
    return jsonify({'msg': 'Token has expired'}), 401


# handle revoked tokens if you implement token revocation for logout functionality
