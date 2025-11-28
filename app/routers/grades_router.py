"""
Grade Router - API endpoints for Grade operations.

Endpoints:
- POST   /grades/                      Create a new grade
- GET    /grades/                      Get all grades
- GET    /grades/{id}                  Get a specific grade
- GET    /grades/enrollment/{id}       Get grade for an enrollment
- PUT    /grades/{id}                  Update a grade
- DELETE /grades/{id}                  Delete a grade
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import GradeCreate, GradeResponse
from app.services import grades_service as grade_service
from pydantic import BaseModel

router = APIRouter()

class GradeUpdate(BaseModel):
    """Schema for updating grade marks."""
    marks: float

@router.post("/", response_model=GradeResponse, status_code=201)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    """
    Create a new grade for an enrollment.
    
    Automatically calculates final_grade (A, B, C, D, F) based on marks.
    Validates marks are between 0-100.
    """
    return grade_service.create_grade(db, grade)

@router.get("/", response_model=List[GradeResponse])
def get_all_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all grades with pagination."""
    return grade_service.get_all_grades(db, skip, limit)

@router.get("/{grade_id}", response_model=GradeResponse)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    """Get a specific grade by ID."""
    return grade_service.get_grade_by_id(db, grade_id)

@router.get("/enrollment/{enrollment_id}", response_model=GradeResponse)
def get_grade_by_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Get the grade for a specific enrollment (student's grade in a course)."""
    return grade_service.get_grade_by_enrollment(db, enrollment_id)

@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(grade_id: int, grade_update: GradeUpdate, db: Session = Depends(get_db)):
    """
    Update a grade's marks.
    
    Automatically recalculates final_grade based on new marks.
    """
    return grade_service.update_grade(db, grade_id, grade_update.marks)

@router.delete("/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    """Delete a grade."""
    return grade_service.delete_grade(db, grade_id)
