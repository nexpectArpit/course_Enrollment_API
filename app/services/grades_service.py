"""
Grade Service - Business logic layer for Grade operations.

This service handles:
- Grade calculation based on marks
- Marks validation (0-100 range)
- Preventing duplicate grades for same enrollment
- Automatic final_grade calculation

Layer Architecture:
Router -> Service -> Repository -> Database
"""

from sqlalchemy.orm import Session
from app.schemas import GradeCreate
from app.repositories import grades_repository as grade_repo
from app.repositories import enrollments_repository as enrollment_repo
from fastapi import HTTPException

def calculate_final_grade(marks: float) -> str:
    """
    Calculate letter grade based on numerical marks.
    
    Grading Scale:
    - 90-100: A (Excellent)
    - 80-89:  B (Good)
    - 70-79:  C (Average)
    - 60-69:  D (Below Average)
    - 0-59:   F (Fail)
    
    Args:
        marks: Numerical marks (0-100)
    
    Returns:
        str: Letter grade (A, B, C, D, or F)
    
    Example:
        calculate_final_grade(95) -> "A"
        calculate_final_grade(75) -> "C"
        calculate_final_grade(55) -> "F"
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
    """
    Create a new grade with validation and automatic calculation.
    
    Business Rules:
    1. Marks must be between 0 and 100
    2. Enrollment must exist
    3. Only one grade per enrollment (no duplicates)
    4. Final grade is automatically calculated from marks
    
    Args:
        db: Database session
        grade: GradeCreate schema with enrollment_id and marks
    
    Returns:
        Grade: Created grade object with calculated final_grade
    
    Raises:
        HTTPException 400: If marks out of range or grade already exists
        HTTPException 404: If enrollment not found
    
    Flow:
        1. Validate marks are in 0-100 range
        2. Check if enrollment exists
        3. Check if grade already exists for this enrollment
        4. Calculate final_grade from marks
        5. Create grade with calculated final_grade
        6. Return created grade
    """
    # Validate marks range (0-100)
    if grade.marks < 0 or grade.marks > 100:
        raise HTTPException(status_code=400, detail="Marks must be between 0 and 100")
    
    # Check if enrollment exists
    enrollment = enrollment_repo.get_enrollment_by_id(db, grade.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Check if grade already exists for this enrollment (prevent duplicates)
    existing_grade = grade_repo.get_grade_by_enrollment(db, grade.enrollment_id)
    if existing_grade:
        raise HTTPException(
            status_code=400, 
            detail="Grade already exists for this enrollment. Use update instead."
        )
    
    # Calculate final grade based on marks
    final_grade = calculate_final_grade(grade.marks)
    
    # Create grade with calculated final_grade
    grade_data = grade.model_dump()
    grade_data['final_grade'] = final_grade
    db_grade = grade_repo.create_grade(db, GradeCreate(**grade_data))
    
    return db_grade

def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all grades with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum records to return
    
    Returns:
        List[Grade]: List of all grades
    """
    return grade_repo.get_all_grades(db, skip, limit)

def get_grade_by_id(db: Session, grade_id: int):
    """
    Get a grade by ID with existence validation.
    
    Args:
        db: Database session
        grade_id: Grade's ID
    
    Returns:
        Grade: Grade object
    
    Raises:
        HTTPException 404: If grade not found
    """
    grade = grade_repo.get_grade_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

def get_grade_by_enrollment(db: Session, enrollment_id: int):
    """
    Get the grade for a specific enrollment.
    
    Business Rules:
    - Enrollment must exist
    - Grade must exist for this enrollment
    
    Args:
        db: Database session
        enrollment_id: Enrollment's ID
    
    Returns:
        Grade: Grade object for this enrollment
    
    Raises:
        HTTPException 404: If enrollment or grade not found
    
    Use Case:
        View a student's grade for a specific course
    """
    # Check if enrollment exists
    enrollment = enrollment_repo.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Get grade for this enrollment
    grade = grade_repo.get_grade_by_enrollment(db, enrollment_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found for this enrollment")
    return grade

def update_grade(db: Session, grade_id: int, marks: float):
    """
    Update a grade's marks and recalculate final_grade.
    
    Business Rules:
    1. Marks must be between 0 and 100
    2. Grade must exist
    3. Final grade is automatically recalculated
    
    Args:
        db: Database session
        grade_id: ID of grade to update
        marks: New numerical marks
    
    Returns:
        Grade: Updated grade object with recalculated final_grade
    
    Raises:
        HTTPException 400: If marks out of range
        HTTPException 404: If grade not found
    
    Flow:
        1. Validate marks are in 0-100 range
        2. Check if grade exists
        3. Recalculate final_grade from new marks
        4. Update grade with new marks and final_grade
        5. Return updated grade
    """
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
    """
    Delete a grade.
    
    Business Rules:
    - Grade must exist
    
    Args:
        db: Database session
        grade_id: ID of grade to delete
    
    Returns:
        dict: Success message
    
    Raises:
        HTTPException 404: If grade not found
        HTTPException 500: If deletion fails
    """
    grade = grade_repo.get_grade_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    success = grade_repo.delete_grade(db, grade_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete grade")
    return {"message": "Grade deleted successfully"}
