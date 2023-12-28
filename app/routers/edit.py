from fastapi import APIRouter

router = APIRouter(prefix="/api/edit", tags=["Edit"])


@router.post("/profile")
async def edit_profile():
    pass


@router.post("/avatar")
async def edit_avatar():
    pass

