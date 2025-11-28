from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import GradeCreate, GradeResponse
from app.services import grades as grade_service
from pydantic import BaseModel

router = APIRouter()

class GradeUpdate(BaseModel):
    marks: float

@router.post("/", response_model=GradeResponse, status_code=201)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    return grade_service.create_grade(db, grade)

@router.get("/", response_model=List[GradeResponse])
def get_all_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return grade_service.get_all_grades(db, skip, limit)

@router.get("/{grade_id}", response_model=GradeResponse)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    return grade_service.get_grade_by_id(db, grade_id)

@router.get("/enrollment/{enrollment_id}", response_model=GradeResponse)
def get_grade_by_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    return grade_service.get_grade_by_enrollment(db, enrollment_id)

@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(grade_id: int, grade_update: GradeUpdate, db: Session = Depends(get_db)):
    return grade_service.update_grade(db, grade_id, grade_update.marks)

@router.delete("/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    return grade_service.delete_grade(db, grade_id)
