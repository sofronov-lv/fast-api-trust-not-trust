from fastapi import APIRouter

user_router = APIRouter(prefix="/api/user", tags=["Adding a user"])


@user_router.get("/registration")
async def registration():
    pass

