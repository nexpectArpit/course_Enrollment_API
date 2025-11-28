"""
SQLAlchemy ORM models for database tables.

This module defines the database schema using SQLAlchemy ORM:
- Student: Stores student information
- Course: Stores course details
- Enrollment: Links students to courses (many-to-many relationship)
- Grade: Stores grades for each enrollment

Relationships:
- One Student can have many Enrollments
- One Course can have many Enrollments
- One Enrollment belongs to one Student and one Course
- One Enrollment has one Grade
"""

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    """
    Student model representing students in the system.
    
    Attributes:
        id: Primary key, auto-incremented
        name: Student's full name
        email: Student's email (must be unique)
        enrollments: List of courses this student is enrolled in
    """
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)  # Unique constraint ensures no duplicate emails
    
    # Relationship: One student can have many enrollments
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    """
    Course model representing courses offered.
    
    Attributes:
        id: Primary key, auto-incremented
        course_name: Full name of the course
        course_code: Unique code identifying the course (e.g., CS101)
        credits: Number of credits for this course
        enrollments: List of students enrolled in this course
    """
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    course_code = Column(String, unique=True, nullable=False)  # Unique constraint ensures no duplicate codes
    credits = Column(Integer, nullable=False)
    
    # Relationship: One course can have many enrollments
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    """
    Enrollment model linking students to courses.
    
    This is the junction table for the many-to-many relationship between
    students and courses. Each enrollment represents one student taking one course.
    
    Attributes:
        id: Primary key, auto-incremented
        student_id: Foreign key to students table
        course_id: Foreign key to courses table
        enrollment_date: Date when student enrolled in the course
        student: Reference to the Student object
        course: Reference to the Course object
        grade: Reference to the Grade object for this enrollment
    """
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    
    # Relationships: Links to Student and Course
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    # uselist=False means one-to-one relationship (one enrollment has one grade)
    grade = relationship("Grade", back_populates="enrollment", uselist=False)

class Grade(Base):
    """
    Grade model storing grades for enrollments.
    
    Each enrollment can have one grade record containing marks and calculated letter grade.
    
    Attributes:
        id: Primary key, auto-incremented
        enrollment_id: Foreign key to enrollments table
        marks: Numerical marks (0-100)
        final_grade: Calculated letter grade (A, B, C, D, F)
        enrollment: Reference to the Enrollment object
    """
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    marks = Column(Float, nullable=False)
    final_grade = Column(String, nullable=True)  # Calculated automatically based on marks
    
    # Relationship: Links back to Enrollment
    enrollment = relationship("Enrollment", back_populates="grade")
