from fastapi.routing import APIRouter


router = APIRouter()

@router.get("/keepa")
async def read_root():
    return {"message": "Hello, Keepa!"}
