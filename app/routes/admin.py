from datetime import timedelta

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from app.auth import admin_required
from app.models import Admin, Book, Student, Loan, BookCategory, db, GradeLevel

admin_bp = Blueprint('admin', __name__)

# authenticated admin route

@admin_bp.post('/login')
def admin_login_required():
    data = request.get_json()
    email = data.get('email')
    password= data.get('password_hash')
    
    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password_hash, password):
        access_token = create_access_token(identity=str(admin.id), additional_claims={'role': 'admin'}, expires_delta=timedelta(hours=24))
        return jsonify({'msg': 'Admin authenticated successfully!', 'access_token': access_token}), 200
    else:
        return jsonify({'msg': 'Invalid email or password'}), 401


# Books and Students management routes

@admin_bp.get('/dashboard')
@jwt_required()
@admin_required
def dashboard():
    # get total books, students, and loans count
    total_books = Book.query.count()
    total_students = Student.query.count()
    total_loans = Loan.query.count()
    return jsonify({
        'msg': 'Welcome to the admin dashboard!',
        'total_books': total_books,
        'total_students': total_students,
        'total_loans': total_loans
    })


# Books management routes

@admin_bp.post('/books/categories/add')
@jwt_required()
@admin_required
def add_category():
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'msg': 'Category name is required!'}), 400
    
    if BookCategory.query.filter_by(name=name).first():
        return jsonify({'msg': 'Category already exists!'}), 400
       
    new_category = BookCategory(name=name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'msg': 'Book category added successfully!'}), 201


@admin_bp.post('/books/categories/update/<int:category_id>')
@jwt_required()
@admin_required
def edit_category(category_id):
    category = BookCategory.query.get_or_404(category_id)
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'msg': 'Category name is required!'}), 400
    category.name = name
    db.session.commit()
    return jsonify({'msg': 'Category updated successfully!'})

@admin_bp.delete('/books/categories/delete/<int:category_id>')
@jwt_required()
@admin_required
def delete_category(category_id):
    category = BookCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'msg': 'Category deleted successfully!'})


@admin_bp.get("/books/all")
# @jwt_required
# @admin_required
def list_books():
    books = Book.query.all()
    
    return jsonify({'books':[book.to_dict() for book in books], 'count': len(books)})


@admin_bp.post('/books/add')
@jwt_required()
@admin_required
def add_book():
    data = request.get_json()
    
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    publisher = data.get('publisher')
    publication_year = data.get('publication_year')
    category_id = data.get('category_id')
    total_copies = data.get('total_copies', 1)
    if not title or not author or not isbn:
        return jsonify({'msg': 'Title, author, and ISBN are required!'}), 400
    if Book.query.filter_by(isbn=isbn).first():
        return jsonify({'msg': 'A book with this ISBN already exists!'}), 400
    new_book = Book(
        title=title,
        author=author,
        isbn=isbn,
        publisher=publisher,
        publication_year=publication_year,
        category_id=category_id,
        total_copies=total_copies,
        available_copies=total_copies
    )
    db.session.add(new_book)
    db.session.commit()
       
    return jsonify({'msg': 'Book added successfully!'}), 201

@admin_bp.put('/books/update/<int:book_id>')
@jwt_required()
@admin_required
def update_book(book_id):
    data = request.get_json()
    
    book = Book.query.get_or_404(book_id)
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.publisher = data.get('publisher', book.publisher)
    book.publication_year = data.get('publication_year', book.publication_year)
    book.category_id = data.get('category_id', book.category_id)
    total_copies = data.get('total_copies', book.total_copies)
    if total_copies < (book.total_copies - book.available_copies):
        return jsonify({'msg': 'Total copies cannot be less than the number of copies currently loaned out!'}), 400
    book.total_copies = total_copies
    book.available_copies = total_copies - (book.total_copies - book.available_copies)
    db.session.commit()
    
    return jsonify({'msg': 'Book updated successfully!'})

@admin_bp.delete('/books/remove/<int:book_id>')
@jwt_required()
@admin_required
def delete_book(book_id):
    # Logic to delete a book from the database
    return jsonify({'msg': 'Book deleted successfully!'})


# Books loans/in libarary use athorization routes

@admin_bp.get('/loans')
@jwt_required()
@admin_required
def view_loans():
    # Logic to retrieve all book loans from the database
    return jsonify({'loans': []})  # Placeholder response

@admin_bp.post('/loans/<int:loan_id>/approve')
@jwt_required()
@admin_required
def approve_loan(loan_id):
    # Logic to approve a loan in the database
    return jsonify({'msg': 'Loan approved successfully!'})

@admin_bp.get('/pending_loans')
@jwt_required()
@admin_required
def view_pending_loans():
    # Logic to retrieve all pending book loans from the database
    return jsonify({'pending_loans': []})  # Placeholder response


@admin_bp.post('/loans/<int:loan_id>/reject')
@jwt_required()
@admin_required
def reject_loan(loan_id):
    # Logic to reject a loan in the database
    return jsonify({'msg': 'Loan rejected successfully!'})


@admin_bp.post('/loans/<int:loan_id>/return')
@jwt_required()
@admin_required
def return_book(loan_id):
    # Logic to mark a loan as returned in the database
    return jsonify({'msg': 'Book returned successfully!'})

# overdue books routes

@admin_bp.get('/loans/overdue')
@jwt_required()
@admin_required
def view_overdue_loans():
    # Logic to retrieve all overdue book loans from the database
    return jsonify({'overdue_loans': []})  # Placeholder response


# students management routes

# students registration 

@admin_bp.post('/register_student')
@jwt_required()
@admin_required

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

# update student information routes
@admin_bp.put('/update_student/<int:student_id>')
@jwt_required()
@admin_required
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get_or_404(student_id)
    
    if not student:
        return jsonify({'msg': 'Student not found!'}), 404
    
    student.firstname = data.get('firstname', student.firstname)
    student.middlename = data.get('middlename', student.middlename)
    student.lastname = data.get('lastname', student.lastname)
    student.email = data.get('email', student.email)
    student.grade_level_id = data.get('grade_level_id', student.grade_level_id)
    
    if data.get('password_hash'):
        student.password_hash = generate_password_hash(data['password_hash'])
    
    db.session.commit()
    
    return jsonify({'msg': 'Student updated successfully!'})

@admin_bp.delete('/delete_student/<int:student_id>')
@jwt_required()
@admin_required
def delete_student(student_id):
    # Logic to delete a student from the database
    return jsonify({'msg': 'Student deleted successfully!'})


# students history

@admin_bp.get('/students/<int:student_id>/history')
@jwt_required()
@admin_required
def student_history(student_id):
    # Logic to retrieve a student's borrowing history from the database
    return jsonify({'history': []})  # Placeholder response


# Libaray membership management routes

@admin_bp.post('/library_membership/<int:student_id>/activate')
@jwt_required()
@admin_required
def activate_membership(student_id):
    # Logic to activate a student's library membership in the database
    return jsonify({'msg': 'Library membership activated successfully!'})

@admin_bp.post('/library_membership/<int:student_id>/deactivate')
@jwt_required()
@admin_required
def deactivate_membership(student_id):
    # Logic to deactivate a student's library membership in the database
    return jsonify({'msg': 'Library membership deactivated successfully!'})

# loans management routes
@admin_bp.get('/loans')
@jwt_required()
@admin_required
def view_loans():
    # Logic to retrieve all book loans from the database
    return jsonify({'loans': []})  # Placeholder response

@admin_bp.post('/loans/<int:loan_id>/approve')
@jwt_required()
@admin_required
def approve_loan(loan_id):
    # Logic to approve a loan in the database
    return jsonify({'msg': 'Loan approved successfully!'})



# Class levels management routes

@admin_bp.post('/class_levels/add')
@jwt_required() 
@admin_required
def add_class_level():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'msg': 'Missing required field: name'}), 400
    new_grade_level = GradeLevel(name=name)
    db.session.add(new_grade_level)
    db.session.commit()
    return jsonify({'msg': 'Class level added successfully!'}), 201