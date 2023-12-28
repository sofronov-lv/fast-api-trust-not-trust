from fastapi import APIRouter

router = APIRouter(prefix="/api/user", tags=["Adding a user"])


@router.post("/registration")
async def registration():
    pass


@router.post("/add")
async def add_user():
    pass
