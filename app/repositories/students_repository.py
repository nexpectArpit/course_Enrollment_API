"""
Student Repository - Database access layer for Student operations.

This module handles all direct database interactions for students.
It uses SQLAlchemy ORM to query and manipulate student records.

Layer Architecture:
Router -> Service -> Repository -> Database

The repository layer:
- Executes SQL queries through SQLAlchemy ORM
- Returns raw database objects
- Does NOT contain business logic or validation
"""

from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate

def create_student(db: Session, student: StudentCreate):
    """
    Create a new student record in the database.
    
    Args:
        db: Database session from get_db()
        student: StudentCreate schema with name and email
    
    Returns:
        Student: Created student object with generated id
    
    Process:
        1. Convert Pydantic schema to dict
        2. Create Student ORM object
        3. Add to session
        4. Commit transaction
        5. Refresh to get generated id
    """
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all students with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
    
    Returns:
        List[Student]: List of student objects
    """
    return db.query(Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, student_id: int):
    """
    Find a student by their ID.
    
    Args:
        db: Database session
        student_id: Student's primary key
    
    Returns:
        Student | None: Student object if found, None otherwise
    """
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    """
    Find a student by their email address.
    
    Used for checking if email already exists before creating/updating.
    
    Args:
        db: Database session
        email: Student's email address
    
    Returns:
        Student | None: Student object if found, None otherwise
    """
    return db.query(Student).filter(Student.email == email).first()

def update_student(db: Session, student_id: int, student: StudentCreate):
    """
    Update an existing student's information.
    
    Args:
        db: Database session
        student_id: ID of student to update
        student: StudentCreate schema with new data
    
    Returns:
        Student | None: Updated student object if found, None otherwise
    
    Process:
        1. Find student by ID
        2. Update fields
        3. Commit changes
        4. Refresh to get updated data
    """
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db_student.name = student.name
        db_student.email = student.email
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    """
    Delete a student from the database (hard delete).
    
    Args:
        db: Database session
        student_id: ID of student to delete
    
    Returns:
        bool: True if deleted successfully, False if not found
    
    Note: This is a hard delete - the record is permanently removed.
    """
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False
