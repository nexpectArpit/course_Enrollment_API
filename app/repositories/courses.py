from sqlalchemy.orm import Session
from app.models import Course
from app.schemas import CourseCreate

def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def get_course_by_code(db: Session, course_code: str):
    return db.query(Course).filter(Course.course_code == course_code).first()

def update_course(db: Session, course_id: int, course: CourseCreate):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db_course.course_name = course.course_name
        db_course.course_code = course.course_code
        db_course.credits = course.credits
        db.commit()
        db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False
