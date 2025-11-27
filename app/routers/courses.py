from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_courses():
    return {"message": "Course routes - coming in Step 2"}
