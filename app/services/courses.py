from sqlalchemy.orm import Session
from app.schemas import CourseCreate
from app.repositories import courses as course_repo
from fastapi import HTTPException

def create_course(db: Session, course: CourseCreate):
    # Check if course code already exists
    existing_course = course_repo.get_course_by_code(db, course.course_code)
    if existing_course:
        raise HTTPException(status_code=400, detail="Course code already exists")
    return course_repo.create_course(db, course)

def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    return course_repo.get_all_courses(db, skip, limit)

def get_course_by_id(db: Session, course_id: int):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

def update_course(db: Session, course_id: int, course: CourseCreate):
    # Check if course exists
    existing_course = course_repo.get_course_by_id(db, course_id)
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if new course code is already taken by another course
    code_check = course_repo.get_course_by_code(db, course.course_code)
    if code_check and code_check.id != course_id:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    return course_repo.update_course(db, course_id, course)

def delete_course(db: Session, course_id: int):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    success = course_repo.delete_course(db, course_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete course")
    return {"message": "Course deleted successfully"}
