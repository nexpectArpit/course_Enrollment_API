from sqlalchemy.orm import Session
from app.schemas import StudentCreate
from app.repositories import students as student_repo
from fastapi import HTTPException

def create_student(db: Session, student: StudentCreate):
    # Check if email already exists
    existing_student = student_repo.get_student_by_email(db, student.email)
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return student_repo.create_student(db, student)

def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    return student_repo.get_all_students(db, skip, limit)

def get_student_by_id(db: Session, student_id: int):
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def update_student(db: Session, student_id: int, student: StudentCreate):
    # Check if student exists
    existing_student = student_repo.get_student_by_id(db, student_id)
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if new email is already taken by another student
    email_check = student_repo.get_student_by_email(db, student.email)
    if email_check and email_check.id != student_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return student_repo.update_student(db, student_id, student)

def delete_student(db: Session, student_id: int):
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    success = student_repo.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete student")
    return {"message": "Student deleted successfully"}
