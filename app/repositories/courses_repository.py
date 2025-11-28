"""
Course Repository - Database access layer for Course operations.

This module handles all direct database interactions for courses.
Similar to students_repository, but for course-related queries.

Layer Architecture:
Router -> Service -> Repository -> Database
"""

from sqlalchemy.orm import Session
from app.models import Course
from app.schemas import CourseCreate

def create_course(db: Session, course: CourseCreate):
    """
    Create a new course record in the database.
    
    Args:
        db: Database session from get_db()
        course: CourseCreate schema with course details
    
    Returns:
        Course: Created course object with generated id
    """
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all courses with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List[Course]: List of course objects
    """
    return db.query(Course).offset(skip).limit(limit).all()

def get_course_by_id(db: Session, course_id: int):
    """
    Find a course by its ID.
    
    Args:
        db: Database session
        course_id: Course's primary key
    
    Returns:
        Course | None: Course object if found, None otherwise
    """
    return db.query(Course).filter(Course.id == course_id).first()

def get_course_by_code(db: Session, course_code: str):
    """
    Find a course by its unique course code.
    
    Used for checking if course code already exists.
    
    Args:
        db: Database session
        course_code: Unique course identifier (e.g., CS101)
    
    Returns:
        Course | None: Course object if found, None otherwise
    """
    return db.query(Course).filter(Course.course_code == course_code).first()

def update_course(db: Session, course_id: int, course: CourseCreate):
    """
    Update an existing course's information.
    
    Args:
        db: Database session
        course_id: ID of course to update
        course: CourseCreate schema with new data
    
    Returns:
        Course | None: Updated course object if found, None otherwise
    """
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db_course.course_name = course.course_name
        db_course.course_code = course.course_code
        db_course.credits = course.credits
        db.commit()
        db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    """
    Delete a course from the database (hard delete).
    
    Args:
        db: Database session
        course_id: ID of course to delete
    
    Returns:
        bool: True if deleted successfully, False if not found
    """
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False
