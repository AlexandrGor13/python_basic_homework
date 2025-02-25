from fastapi import APIRouter

router = APIRouter()

@router.get('/about')
def about():
    return {"message": "Welcome to the homework4 application!"}