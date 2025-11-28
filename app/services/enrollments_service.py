"""
Enrollment Service - Business logic layer for Enrollment operations.

This service handles the complex business rules for enrollments:
- Validates that both student and course exist
- Prevents duplicate enrollments
- Manages the relationship between students and courses

Layer Architecture:
Router -> Service -> Repository -> Database
"""

from sqlalchemy.orm import Session
from app.schemas import EnrollmentCreate
from app.repositories import enrollments_repository as enrollment_repo
from app.repositories import students_repository as student_repo
from app.repositories import courses_repository as course_repo
from fastapi import HTTPException

def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    """
    Create a new enrollment with comprehensive validation.
    
    Business Rules:
    1. Student must exist
    2. Course must exist
    3. Student cannot be enrolled in the same course twice (no duplicates)
    
    Args:
        db: Database session
        enrollment: EnrollmentCreate schema with student_id, course_id, date
    
    Returns:
        Enrollment: Created enrollment object
    
    Raises:
        HTTPException 404: If student or course not found
        HTTPException 400: If student already enrolled in this course
    
    Flow:
        1. Validate student exists (call students_repository)
        2. Validate course exists (call courses_repository)
        3. Check for duplicate enrollment (call enrollments_repository)
        4. If all validations pass, create enrollment
        5. Return created enrollment
    """
    # Check if student exists
    student = student_repo.get_student_by_id(db, enrollment.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if course exists
    course = course_repo.get_course_by_id(db, enrollment.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check for duplicate enrollment (student already enrolled in this course)
    existing_enrollment = enrollment_repo.get_enrollment_by_student_and_course(
        db, enrollment.student_id, enrollment.course_id
    )
    if existing_enrollment:
        raise HTTPException(
            status_code=400, 
            detail="Student is already enrolled in this course"
        )
    
    return enrollment_repo.create_enrollment(db, enrollment)

def get_all_enrollments(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all enrollments with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum records to return
    
    Returns:
        List[Enrollment]: List of all enrollments
    """
    return enrollment_repo.get_all_enrollments(db, skip, limit)

def get_enrollment_by_id(db: Session, enrollment_id: int):
    """
    Get an enrollment by ID with existence validation.
    
    Args:
        db: Database session
        enrollment_id: Enrollment's ID
    
    Returns:
        Enrollment: Enrollment object
    
    Raises:
        HTTPException 404: If enrollment not found
    """
    enrollment = enrollment_repo.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

def get_enrollments_by_student(db: Session, student_id: int):
    """
    Get all courses a student is enrolled in.
    
    Business Rules:
    - Student must exist
    
    Args:
        db: Database session
        student_id: Student's ID
    
    Returns:
        List[Enrollment]: All enrollments for this student
    
    Raises:
        HTTPException 404: If student not found
    
    Use Case:
        View all courses a specific student is taking
    """
    # Check if student exists
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return enrollment_repo.get_enrollments_by_student(db, student_id)

def get_enrollments_by_course(db: Session, course_id: int):
    """
    Get all students enrolled in a specific course.
    
    Business Rules:
    - Course must exist
    
    Args:
        db: Database session
        course_id: Course's ID
    
    Returns:
        List[Enrollment]: All enrollments for this course
    
    Raises:
        HTTPException 404: If course not found
    
    Use Case:
        View all students taking a specific course (class roster)
    """
    # Check if course exists
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return enrollment_repo.get_enrollments_by_course(db, course_id)

def delete_enrollment(db: Session, enrollment_id: int):
    """
    Delete an enrollment (unenroll a student from a course).
    
    Business Rules:
    - Enrollment must exist
    
    Args:
        db: Database session
        enrollment_id: ID of enrollment to delete
    
    Returns:
        dict: Success message
    
    Raises:
        HTTPException 404: If enrollment not found
        HTTPException 500: If deletion fails
    """
    enrollment = enrollment_repo.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    success = enrollment_repo.delete_enrollment(db, enrollment_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete enrollment")
    return {"message": "Enrollment deleted successfully"}
