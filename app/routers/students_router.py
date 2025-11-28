"""
Student Router - API endpoints for Student operations.

This module defines the REST API endpoints for student management.
It handles HTTP requests and responses, delegates business logic to the service layer.

Layer Architecture:
Router (this file) -> Service -> Repository -> Database

Endpoints:
- POST   /students/          Create a new student
- GET    /students/          Get all students (with pagination)
- GET    /students/{id}      Get a specific student by ID
- PUT    /students/{id}      Update a student
- DELETE /students/{id}      Delete a student
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import StudentCreate, StudentResponse
from app.services import students_service as student_service

# Create router instance
# This will be included in main.py with prefix="/students"
router = APIRouter()

@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Create a new student.
    
    Request Body:
        {
            "name": "John Doe",
            "email": "john@example.com"
        }
    
    Response: 201 Created
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        }
    
    Errors:
        - 400: Email already registered
    """
    return student_service.create_student(db, student)

@router.get("/", response_model=List[StudentResponse])
def get_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all students with pagination.
    
    Query Parameters:
        - skip: Number of records to skip (default: 0)
        - limit: Maximum records to return (default: 100)
    
    Response: 200 OK
        [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ]
    """
    return student_service.get_all_students(db, skip, limit)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Get a specific student by ID.
    
    Path Parameter:
        - student_id: Student's ID
    
    Response: 200 OK
        {"id": 1, "name": "John Doe", "email": "john@example.com"}
    
    Errors:
        - 404: Student not found
    """
    return student_service.get_student_by_id(db, student_id)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    """
    Update an existing student.
    
    Path Parameter:
        - student_id: Student's ID
    
    Request Body:
        {
            "name": "John Doe Updated",
            "email": "john.new@example.com"
        }
    
    Response: 200 OK
        {"id": 1, "name": "John Doe Updated", "email": "john.new@example.com"}
    
    Errors:
        - 404: Student not found
        - 400: Email already registered by another student
    """
    return student_service.update_student(db, student_id, student)

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Delete a student.
    
    Path Parameter:
        - student_id: Student's ID
    
    Response: 200 OK
        {"message": "Student deleted successfully"}
    
    Errors:
        - 404: Student not found
    """
    return student_service.delete_student(db, student_id)
