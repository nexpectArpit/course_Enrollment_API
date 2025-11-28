"""
Enrollment Router - API endpoints for Enrollment operations.

Endpoints:
- POST   /enrollments/                  Create a new enrollment
- GET    /enrollments/                  Get all enrollments
- GET    /enrollments/{id}              Get a specific enrollment
- GET    /enrollments/student/{id}      Get all enrollments for a student
- GET    /enrollments/course/{id}       Get all enrollments for a course
- DELETE /enrollments/{id}              Delete an enrollment
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import EnrollmentCreate, EnrollmentResponse
from app.services import enrollments_service as enrollment_service

router = APIRouter()

@router.post("/", response_model=EnrollmentResponse, status_code=201)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    """
    Create a new enrollment (enroll a student in a course).
    
    Validates that student and course exist, and prevents duplicate enrollments.
    """
    return enrollment_service.create_enrollment(db, enrollment)

@router.get("/", response_model=List[EnrollmentResponse])
def get_all_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all enrollments with pagination."""
    return enrollment_service.get_all_enrollments(db, skip, limit)

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Get a specific enrollment by ID."""
    return enrollment_service.get_enrollment_by_id(db, enrollment_id)

@router.get("/student/{student_id}", response_model=List[EnrollmentResponse])
def get_enrollments_by_student(student_id: int, db: Session = Depends(get_db)):
    """Get all courses a student is enrolled in."""
    return enrollment_service.get_enrollments_by_student(db, student_id)

@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])
def get_enrollments_by_course(course_id: int, db: Session = Depends(get_db)):
    """Get all students enrolled in a course (class roster)."""
    return enrollment_service.get_enrollments_by_course(db, course_id)

@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Delete an enrollment (unenroll a student from a course)."""
    return enrollment_service.delete_enrollment(db, enrollment_id)
