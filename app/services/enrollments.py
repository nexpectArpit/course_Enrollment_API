from sqlalchemy.orm import Session
from app.schemas import EnrollmentCreate
from app.repositories import enrollments as enrollment_repo
from app.repositories import students as student_repo
from app.repositories import courses as course_repo
from fastapi import HTTPException

def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    # Check if student exists
    student = student_repo.get_student_by_id(db, enrollment.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if course exists
    course = course_repo.get_course_by_id(db, enrollment.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check for duplicate enrollment
    existing_enrollment = enrollment_repo.get_enrollment_by_student_and_course(
        db, enrollment.student_id, enrollment.course_id
    )
    if existing_enrollment:
        raise HTTPException(
            status_code=400, 
            detail="Student is already enrolled in this course"
        )
    
    return enrollment_repo.create_enrollment(db, enrollment)

def get_all_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return enrollment_repo.get_all_enrollments(db, skip, limit)

def get_enrollment_by_id(db: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

def get_enrollments_by_student(db: Session, student_id: int):
    # Check if student exists
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return enrollment_repo.get_enrollments_by_student(db, student_id)

def get_enrollments_by_course(db: Session, course_id: int):
    # Check if course exists
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return enrollment_repo.get_enrollments_by_course(db, course_id)

def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = enrollment_repo.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    success = enrollment_repo.delete_enrollment(db, enrollment_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete enrollment")
    return {"message": "Enrollment deleted successfully"}
