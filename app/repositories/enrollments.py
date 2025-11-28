from sqlalchemy.orm import Session
from app.models import Enrollment
from app.schemas import EnrollmentCreate

def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_all_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Enrollment).offset(skip).limit(limit).all()

def get_enrollment_by_id(db: Session, enrollment_id: int):
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

def get_enrollment_by_student_and_course(db: Session, student_id: int, course_id: int):
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()

def get_enrollments_by_student(db: Session, student_id: int):
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).all()

def get_enrollments_by_course(db: Session, course_id: int):
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()

def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
        return True
    return False
