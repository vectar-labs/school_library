from flask import Blueprint, request, jsonify
from app.models import Student, Book, Loan
from app.models import db
from werkzeug.security import check_password_hash, generate_password_hash
from app.auth import student_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_identity, jwt_required

student_bp = Blueprint('student', __name__)


# students registration 

@student_bp.post('/register')

def register():
    data = request.get_json()
    
    firstname = data.get('firstname')
    middlename = data.get('middlename')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password_hash')
    grade_level_id = data.get('grade_level_id')
    role = 'student'
    
    if not all([firstname, lastname, email, password]):
        return jsonify({'msg': 'Missing required fields!'}), 400
    
    if Student.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email already registered!'}), 400
    
    new_student = Student(
        firstname=firstname,
        middlename=middlename,
        lastname=lastname,
        email=email,
        password_hash=generate_password_hash(password),  # In production, hash the password before storing
        grade_level_id=grade_level_id,
        role=role
    )
    db.session.add(new_student)
    db.session.commit()
        
    
    return jsonify({'msg': 'Student registered successfully!'}), 201



@student_bp.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password_hash')
    student = Student.query.filter_by(email=email).first()
    if not student or not check_password_hash(student.password_hash, password):
        return jsonify({'msg': 'Invalid email or password!'}), 401
    
    access_token = create_access_token(identity=str(student.id), additional_claims={'role': student.role})
    return jsonify({'msg': 'Login successful!', 'token': access_token}), 200


@student_bp.get('/profile')
@jwt_required()
@student_required
def view_profile():
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'msg': 'Student not found!'}), 404
    
    return jsonify({
        'firstname': student.firstname,
        'middlename': student.middlename,
        'lastname': student.lastname,
        'email': student.email,
        'grade_level_id': student.grade_level_id
    }), 200
    
@student_bp.put('/logout')
@jwt_required()
@student_required
def logout():
    
    return jsonify({'msg': 'Logout successful!'}), 200

# book borrowing routes

# get a list of books available for borrowing
@student_bp.get('/books')
def view_books():
    # Logic to retrieve all available books from the database
    return jsonify({'books': []})  # Placeholder response

#  get specific book details
@student_bp.get('/books/<int:book_id>')
def view_book_details(book_id):
    # Logic to retrieve specific book details from the database
    return jsonify({'book': {}})  # Placeholder response


#  Borrow a book operations

@student_bp.post('/loans')
def borrow_book_request():
    return jsonify({'msg': 'Book loan request submitted successfully!'})


@student_bp.get('/loans_history')
def view_loans_history():
    # Logic to retrieve the student's borrowing history from the database
    return jsonify({'loans_history': []})  # Placeholder response