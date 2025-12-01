from pydantic import BaseModel
from datetime import date
from typing import Optional

class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    
    class Config:
        from_attributes = True

# Course schemas
class CourseBase(BaseModel):
    course_name: str
    course_code: str
    credits: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    
    class Config:
        from_attributes = True

# Enrollment schemas
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    
    class Config:
        from_attributes = True

# Grade schemas
class GradeBase(BaseModel):
    enrollment_id: int
    marks: float
    final_grade: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class GradeResponse(GradeBase):
    id: int
    
    class Config:
        from_attributes = True
