"""
Main application file for Course Enrollment API.

This file initializes the FastAPI application and sets up:
- Database connection and table creation
- API routers for different modules
- Health check endpoint
"""

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import students_router, courses_router, enrollments_router, grades_router
from app import models

# Create all database tables on startup
# This reads the SQLAlchemy models and creates corresponding tables in PostgreSQL
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Course Enrollment API",
    description="API for managing student course enrollments and grades",
    version="1.0.0"
)

# Health check endpoint - used to verify API is running
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify API status.
    Returns a simple JSON response indicating the API is operational.
    """
    return {"status": "healthy", "message": "Course Enrollment API is running"}

# Include routers for different modules
# Each router handles a specific domain (students, courses, enrollments, grades)
# prefix: URL prefix for all routes in this router
# tags: Used for grouping endpoints in Swagger UI documentation
app.include_router(students_router.router, prefix="/students", tags=["Students"])
app.include_router(courses_router.router, prefix="/courses", tags=["Courses"])
app.include_router(enrollments_router.router, prefix="/enrollments", tags=["Enrollments"])
app.include_router(grades_router.router, prefix="/grades", tags=["Grades"])
