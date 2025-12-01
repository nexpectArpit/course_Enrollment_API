from fastapi import FastAPI
from app.database import engine, Base
from app.routers import students_router, courses_router, enrollments_router, grades_router
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Enrollment API",
    description="API for managing student course enrollments and grades",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Course Enrollment API is running"}

app.include_router(students_router.router, prefix="/students", tags=["Students"])
app.include_router(courses_router.router, prefix="/courses", tags=["Courses"])
app.include_router(enrollments_router.router, prefix="/enrollments", tags=["Enrollments"])
app.include_router(grades_router.router, prefix="/grades", tags=["Grades"])
