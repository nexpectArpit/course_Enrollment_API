"""
Course Router - API endpoints for Course operations.

Endpoints:
- POST   /courses/          Create a new course
- GET    /courses/          Get all courses
- GET    /courses/{id}      Get a specific course
- PUT    /courses/{id}      Update a course
- DELETE /courses/{id}      Delete a course
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import CourseCreate, CourseResponse
from app.services import courses_service as course_service

router = APIRouter()

@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course."""
    return course_service.create_course(db, course)

@router.get("/", response_model=List[CourseResponse])
def get_all_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all courses with pagination."""
    return course_service.get_all_courses(db, skip, limit)

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a specific course by ID."""
    return course_service.get_course_by_id(db, course_id)

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    """Update an existing course."""
    return course_service.update_course(db, course_id, course)

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Delete a course."""
    return course_service.delete_course(db, course_id)
