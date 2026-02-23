from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)  # Removed unique=True - names shouldn't be unique
    middlename = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=False)   # Removed unique=True
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='admin')
    password_hash = db.Column(db.String(256), nullable=False)  # Increased length for modern hashes
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class GradeLevel(db.Model):
    __tablename__ = 'grade_levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Student(db.Model):
    __tablename__ = 'students'  # Changed from 'users' to be consistent
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)  # Removed unique=True
    middlename = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(80), nullable=False)   # Removed unique=True
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student')
    grade_level_id = db.Column(db.Integer, db.ForeignKey('grade_levels.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    grade_level = db.relationship('GradeLevel', backref='students')
    loans = db.relationship('Loan', foreign_keys='Loan.student_id', backref='student')
    library_memberships = db.relationship('LibraryMember', backref='student')

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'grade_level_id': self.grade_level_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class BookCategory(db.Model):  # Fixed typo: was BoookCategory
    __tablename__ = 'book_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationship
    books = db.relationship('Book', backref='category')


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('book_categories.id'), nullable=True)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)

    # Relationships
    loans = db.relationship('Loan', backref='book')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'available_copies': self.available_copies
        }


class LibraryMember(db.Model):
    __tablename__ = 'library_members'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # Changed from user_id
    membership_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    loans = db.relationship('Loan', backref='library_member')


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # Changed from user_id
    library_member_id = db.Column(db.Integer, db.ForeignKey('library_members.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_request_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    approved_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)  # Added due date
    status = db.Column(db.String(20), default='pending')  # pending, approved, borrowed, returned, rejected, overdue
    
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)  # Changed to admins.id
    approved_by = db.relationship('Admin', foreign_keys=[admin_id])  # Changed to Admin model

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'book_id': self.book_id,
            'loan_request_date': self.loan_request_date.isoformat() if self.loan_request_date else None,
            'approved_date': self.approved_date.isoformat() if self.approved_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status,
            'approved_by': self.approved_by.firstname if self.approved_by else None
        }


class InLibraryUse(db.Model):
    __tablename__ = 'in_library_uses'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # Changed from user_id
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    use_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    end_time = db.Column(db.DateTime, nullable=True)  # Added end time for tracking
    
    # Relationships
    student = db.relationship('Student', backref='in_library_uses')
    book = db.relationship('Book', backref='in_library_uses')