from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_grades():
    return {"message": "Grade routes - coming in Step 3"}
