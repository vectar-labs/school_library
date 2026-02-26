import datetime
from time import timezone

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
@jwt_required()
@student_required
def view_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'available_copies': book.available_copies
        })
    return jsonify({'books': book_list})    

#  get specific book details
@student_bp.get('/books/<int:book_id>')
@jwt_required()
@student_required
def view_book_details(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'msg': 'Book not found!'}), 404
    
    return jsonify({
        'book': {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'available_copies': book.available_copies
        }
    })


#  Borrow a book operations

@student_bp.post('/loans/<int:book_id>/borrow')
@jwt_required()
@student_required
def borrow_book_request(book_id):
    student_id = get_jwt_identity()
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'msg': 'Book not found!'}), 404
    
    if book.available_copies <= 0:
        return jsonify({'msg': 'Book is not available for borrowing!'}), 400
    
    new_loan = {
        'student_id': student_id,
        'library_member_id': None,
        'loan_request_date': datetime.now(timezone.utc),
        'approved_date': None,
        'return_date': None,
        'due_date': None,  
        'admin_id': None,  
        'approved_by': None,  
        'book_id': book_id,
        'status': 'pending'
        
    }
    db.session.add(new_loan)
    db.session.commit()
    
    return jsonify({'msg': 'Book loan request submitted successfully!'}), 201


@student_bp.get('/loans_history')
def view_loans_history():
    # Logic to retrieve the student's borrowing history from the database
    return jsonify({'loans_history': []})  # Placeholder response