from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

def update_student(db: Session, student_id: int, student: StudentCreate):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db_student.name = student.name
        db_student.email = student.email
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False
