from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_enrollments():
    return {"message": "Enrollment routes - coming in Step 3"}
