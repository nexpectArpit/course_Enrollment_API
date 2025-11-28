"""
Enrollment Repository - Database access layer for Enrollment operations.

This module handles database queries for enrollments (student-course relationships).
Enrollments link students to courses in a many-to-many relationship.

Layer Architecture:
Router -> Service -> Repository -> Database
"""

from sqlalchemy.orm import Session
from app.models import Enrollment
from app.schemas import EnrollmentCreate

def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    """
    Create a new enrollment record linking a student to a course.
    
    Args:
        db: Database session
        enrollment: EnrollmentCreate schema with student_id, course_id, date
    
    Returns:
        Enrollment: Created enrollment object with generated id
    """
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_all_enrollments(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all enrollments with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List[Enrollment]: List of enrollment objects
    """
    return db.query(Enrollment).offset(skip).limit(limit).all()

def get_enrollment_by_id(db: Session, enrollment_id: int):
    """
    Find an enrollment by its ID.
    
    Args:
        db: Database session
        enrollment_id: Enrollment's primary key
    
    Returns:
        Enrollment | None: Enrollment object if found, None otherwise
    """
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

def get_enrollment_by_student_and_course(db: Session, student_id: int, course_id: int):
    """
    Find an enrollment for a specific student-course combination.
    
    Used to check if a student is already enrolled in a course
    (prevents duplicate enrollments).
    
    Args:
        db: Database session
        student_id: Student's ID
        course_id: Course's ID
    
    Returns:
        Enrollment | None: Enrollment if exists, None otherwise
    """
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()

def get_enrollments_by_student(db: Session, student_id: int):
    """
    Get all courses a student is enrolled in.
    
    Args:
        db: Database session
        student_id: Student's ID
    
    Returns:
        List[Enrollment]: All enrollments for this student
    """
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).all()

def get_enrollments_by_course(db: Session, course_id: int):
    """
    Get all students enrolled in a specific course.
    
    Args:
        db: Database session
        course_id: Course's ID
    
    Returns:
        List[Enrollment]: All enrollments for this course
    """
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()

def delete_enrollment(db: Session, enrollment_id: int):
    """
    Delete an enrollment (unenroll a student from a course).
    
    Args:
        db: Database session
        enrollment_id: ID of enrollment to delete
    
    Returns:
        bool: True if deleted successfully, False if not found
    """
    db_enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
        return True
    return False
