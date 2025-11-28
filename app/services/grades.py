from sqlalchemy.orm import Session
from app.schemas import GradeCreate
from app.repositories import grades as grade_repo
from app.repositories import enrollments as enrollment_repo
from fastapi import HTTPException

def calculate_final_grade(marks: float) -> str:
    """
    Calculate final grade based on marks
    90-100 = A
    80-89 = B
    70-79 = C
    60-69 = D
    <60 = F
    """
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    else:
        return "F"

def create_grade(db: Session, grade: GradeCreate):
    # Validate marks range
    if grade.marks < 0 or grade.marks > 100:
        raise HTTPException(status_code=400, detail="Marks must be between 0 and 100")
    
    # Check if enrollment exists
    enrollment = enrollment_repo.get_enrollment_by_id(db, grade.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Check if grade already exists for this enrollment
    existing_grade = grade_repo.get_grade_by_enrollment(db, grade.enrollment_id)
    if existing_grade:
        raise HTTPException(
            status_code=400, 
            detail="Grade already exists for this enrollment. Use update instead."
        )
    
    # Calculate final grade
    final_grade = calculate_final_grade(grade.marks)
    
    # Create grade with calculated final_grade
    grade_data = grade.model_dump()
    grade_data['final_grade'] = final_grade
    db_grade = grade_repo.create_grade(db, GradeCreate(**grade_data))
    
    return db_grade

def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    return grade_repo.get_all_grades(db, skip, limit)

def get_grade_by_id(db: Session, grade_id: int):
    grade = grade_repo.get_grade_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

def get_grade_by_enrollment(db: Session, enrollment_id: int):
    # Check if enrollment exists
    enrollment = enrollment_repo.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    grade = grade_repo.get_grade_by_enrollment(db, enrollment_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found for this enrollment")
    return grade

def update_grade(db: Session, grade_id: int, marks: float):
    # Validate marks range
    if marks < 0 or marks > 100:
        raise HTTPException(status_code=400, detail="Marks must be between 0 and 100")
    
    # Check if grade exists
    grade = grade_repo.get_grade_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    # Calculate new final grade
    final_grade = calculate_final_grade(marks)
    
    return grade_repo.update_grade(db, grade_id, marks, final_grade)

def delete_grade(db: Session, grade_id: int):
    grade = grade_repo.get_grade_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    success = grade_repo.delete_grade(db, grade_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete grade")
    return {"message": "Grade deleted successfully"}
