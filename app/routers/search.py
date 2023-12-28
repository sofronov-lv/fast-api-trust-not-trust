from fastapi import APIRouter

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/contacts")
async def get_contacts():
    pass


@router.get("/normal")
async def get_users():
    pass


@router.get("/advanced")
async def get_users():
    pass


@router.get("/evaluators")
async def get_evaluators():
    pass
