from fastapi import APIRouter

router = APIRouter(prefix="/api/rate", tags=["Rate"])


@router.get("/rating")
async def get_rating():
    pass


@router.post("/user")
async def rate_user():
    pass
