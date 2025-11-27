from fastapi import FastAPI
from app.database import engine, Base
from app.routers import students, courses, enrollments, grades

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Enrollment API",
    description="API for managing student course enrollments and grades",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Course Enrollment API is running"}

# Include routers
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])
app.include_router(grades.router, prefix="/grades", tags=["Grades"])
