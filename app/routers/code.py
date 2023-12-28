from fastapi import APIRouter

user_router = APIRouter(prefix="/api/code", tags=["Code"])


@user_router.get("/")
async def registration():
    pass
