from sqlalchemy.orm import Session
from app.models import Grade
from app.schemas import GradeCreate

def create_grade(db: Session, grade: GradeCreate):
    db_grade = Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Grade).offset(skip).limit(limit).all()

def get_grade_by_id(db: Session, grade_id: int):
    return db.query(Grade).filter(Grade.id == grade_id).first()

def get_grade_by_enrollment(db: Session, enrollment_id: int):
    return db.query(Grade).filter(Grade.enrollment_id == enrollment_id).first()

def update_grade(db: Session, grade_id: int, marks: float, final_grade: str):
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        db_grade.marks = marks
        db_grade.final_grade = final_grade
        db.commit()
        db.refresh(db_grade)
    return db_grade

def delete_grade(db: Session, grade_id: int):
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        db.delete(db_grade)
        db.commit()
        return True
    return False
