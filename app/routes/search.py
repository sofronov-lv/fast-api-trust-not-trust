from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.schemas.user_schemas import UserOut, UserCreate, UserUpdatePartial, UserContactList

from app.database.models import db_helper


router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/", response_model=list[UserOut])
async def get_users(
        offset: int = 0,
        limit: int = 10,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_users(session, offset, limit)


@router.post("/contacts", response_model=list[UserOut])
async def get_contacts(
        contacts: UserContactList,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_contact_list(session, contacts)


@router.post("/normal", response_model=list[UserOut])
async def get_users():
    pass


@router.post("/advanced", response_model=list[UserOut])
async def get_users():
    pass


@router.post("/evaluators", response_model=list[UserOut])
async def get_evaluators():
    pass
