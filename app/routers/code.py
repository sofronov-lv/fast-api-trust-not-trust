from fastapi import APIRouter

router = APIRouter(prefix="/api/code", tags=["Code"])


@router.get("/")
async def get_code():
    pass


@router.post("/")
async def post_code():
    pass
