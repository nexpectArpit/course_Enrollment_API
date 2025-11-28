"""
Student Service - Business logic layer for Student operations.

This module contains business logic and validation for student operations.
It sits between the router (API layer) and repository (database layer).

Layer Architecture:
Router (API endpoints) -> Service (business logic) -> Repository (database queries)

The service layer:
- Validates business rules (e.g., email uniqueness)
- Handles error cases and raises appropriate HTTP exceptions
- Calls repository functions for database operations
- Does NOT directly interact with the database
"""

from sqlalchemy.orm import Session
from app.schemas import StudentCreate
from app.repositories import students_repository as student_repo
from fastapi import HTTPException

def create_student(db: Session, student: StudentCreate):
    """
    Create a new student with email validation.
    
    Business Rules:
    - Email must be unique across all students
    
    Args:
        db: Database session
        student: StudentCreate schema with name and email
    
    Returns:
        Student: Created student object
    
    Raises:
        HTTPException 400: If email already exists
    
    Flow:
        1. Check if email already exists (call repository)
        2. If exists, raise 400 error
        3. If not, create student (call repository)
        4. Return created student
    """
    # Check if email already exists
    existing_student = student_repo.get_student_by_email(db, student.email)
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return student_repo.create_student(db, student)

def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all students with pagination.
    
    No business logic needed here, just pass through to repository.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum records to return
    
    Returns:
        List[Student]: List of all students
    """
    return student_repo.get_all_students(db, skip, limit)

def get_student_by_id(db: Session, student_id: int):
    """
    Get a student by ID with existence validation.
    
    Business Rules:
    - Student must exist
    
    Args:
        db: Database session
        student_id: Student's ID
    
    Returns:
        Student: Student object
    
    Raises:
        HTTPException 404: If student not found
    
    Flow:
        1. Try to find student (call repository)
        2. If not found, raise 404 error
        3. If found, return student
    """
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def update_student(db: Session, student_id: int, student: StudentCreate):
    """
    Update a student with validation.
    
    Business Rules:
    - Student must exist
    - New email must be unique (not used by another student)
    
    Args:
        db: Database session
        student_id: ID of student to update
        student: StudentCreate schema with new data
    
    Returns:
        Student: Updated student object
    
    Raises:
        HTTPException 404: If student not found
        HTTPException 400: If new email already taken by another student
    
    Flow:
        1. Check if student exists
        2. Check if new email is taken by another student
        3. If validations pass, update student
        4. Return updated student
    """
    # Check if student exists
    existing_student = student_repo.get_student_by_id(db, student_id)
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if new email is already taken by another student
    email_check = student_repo.get_student_by_email(db, student.email)
    if email_check and email_check.id != student_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return student_repo.update_student(db, student_id, student)

def delete_student(db: Session, student_id: int):
    """
    Delete a student with existence validation.
    
    Business Rules:
    - Student must exist
    
    Args:
        db: Database session
        student_id: ID of student to delete
    
    Returns:
        dict: Success message
    
    Raises:
        HTTPException 404: If student not found
        HTTPException 500: If deletion fails
    
    Flow:
        1. Check if student exists
        2. Try to delete student
        3. Return success message
    """
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    success = student_repo.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete student")
    return {"message": "Student deleted successfully"}
