from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_students():
    return {"message": "Student routes - coming in Step 2"}
