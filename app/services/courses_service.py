"""
Course Service - Business logic layer for Course operations.

Similar to students_service, but handles course-specific business rules.

Layer Architecture:
Router -> Service -> Repository -> Database
"""

from sqlalchemy.orm import Session
from app.schemas import CourseCreate
from app.repositories import courses_repository as course_repo
from fastapi import HTTPException

def create_course(db: Session, course: CourseCreate):
    """
    Create a new course with course code validation.
    
    Business Rules:
    - Course code must be unique across all courses
    
    Args:
        db: Database session
        course: CourseCreate schema with course details
    
    Returns:
        Course: Created course object
    
    Raises:
        HTTPException 400: If course code already exists
    """
    # Check if course code already exists
    existing_course = course_repo.get_course_by_code(db, course.course_code)
    if existing_course:
        raise HTTPException(status_code=400, detail="Course code already exists")
    return course_repo.create_course(db, course)

def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all courses with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum records to return
    
    Returns:
        List[Course]: List of all courses
    """
    return course_repo.get_all_courses(db, skip, limit)

def get_course_by_id(db: Session, course_id: int):
    """
    Get a course by ID with existence validation.
    
    Business Rules:
    - Course must exist
    
    Args:
        db: Database session
        course_id: Course's ID
    
    Returns:
        Course: Course object
    
    Raises:
        HTTPException 404: If course not found
    """
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

def update_course(db: Session, course_id: int, course: CourseCreate):
    """
    Update a course with validation.
    
    Business Rules:
    - Course must exist
    - New course code must be unique (not used by another course)
    
    Args:
        db: Database session
        course_id: ID of course to update
        course: CourseCreate schema with new data
    
    Returns:
        Course: Updated course object
    
    Raises:
        HTTPException 404: If course not found
        HTTPException 400: If new course code already taken
    """
    # Check if course exists
    existing_course = course_repo.get_course_by_id(db, course_id)
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if new course code is already taken by another course
    code_check = course_repo.get_course_by_code(db, course.course_code)
    if code_check and code_check.id != course_id:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    return course_repo.update_course(db, course_id, course)

def delete_course(db: Session, course_id: int):
    """
    Delete a course with existence validation.
    
    Business Rules:
    - Course must exist
    
    Args:
        db: Database session
        course_id: ID of course to delete
    
    Returns:
        dict: Success message
    
    Raises:
        HTTPException 404: If course not found
        HTTPException 500: If deletion fails
    """
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    success = course_repo.delete_course(db, course_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete course")
    return {"message": "Course deleted successfully"}
