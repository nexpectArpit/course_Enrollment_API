"""
Grade Repository - Database access layer for Grade operations.

This module handles database queries for grades.
Each grade is linked to an enrollment (one grade per enrollment).

Layer Architecture:
Router -> Service -> Repository -> Database
"""

from sqlalchemy.orm import Session
from app.models import Grade
from app.schemas import GradeCreate

def create_grade(db: Session, grade: GradeCreate):
    """
    Create a new grade record for an enrollment.
    
    Args:
        db: Database session
        grade: GradeCreate schema with enrollment_id, marks, final_grade
    
    Returns:
        Grade: Created grade object with generated id
    """
    db_grade = Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all grades with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List[Grade]: List of grade objects
    """
    return db.query(Grade).offset(skip).limit(limit).all()

def get_grade_by_id(db: Session, grade_id: int):
    """
    Find a grade by its ID.
    
    Args:
        db: Database session
        grade_id: Grade's primary key
    
    Returns:
        Grade | None: Grade object if found, None otherwise
    """
    return db.query(Grade).filter(Grade.id == grade_id).first()

def get_grade_by_enrollment(db: Session, enrollment_id: int):
    """
    Find the grade for a specific enrollment.
    
    Used to check if a grade already exists for an enrollment
    (prevents duplicate grades).
    
    Args:
        db: Database session
        enrollment_id: Enrollment's ID
    
    Returns:
        Grade | None: Grade if exists, None otherwise
    """
    return db.query(Grade).filter(Grade.enrollment_id == enrollment_id).first()

def update_grade(db: Session, grade_id: int, marks: float, final_grade: str):
    """
    Update an existing grade's marks and letter grade.
    
    Args:
        db: Database session
        grade_id: ID of grade to update
        marks: New numerical marks (0-100)
        final_grade: New calculated letter grade (A, B, C, D, F)
    
    Returns:
        Grade | None: Updated grade object if found, None otherwise
    """
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        db_grade.marks = marks
        db_grade.final_grade = final_grade
        db.commit()
        db.refresh(db_grade)
    return db_grade

def delete_grade(db: Session, grade_id: int):
    """
    Delete a grade from the database.
    
    Args:
        db: Database session
        grade_id: ID of grade to delete
    
    Returns:
        bool: True if deleted successfully, False if not found
    """
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        db.delete(db_grade)
        db.commit()
        return True
    return False
