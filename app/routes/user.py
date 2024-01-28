from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes import utils

from app.routes.schemas.user_schemas import UserOut, UserUpdatePartial, UserRegistration

from app.routes.services import auth_service
from app.routes.services import user_service

from app.database.models import db_helper
from app.database.models import User

router = APIRouter(prefix="/api/user", tags=["Users"])


@router.get("/avatar")
async def get_avatar(
        user_id: int,
        auth: UserOut = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return {"status": "ok", "url": f"http://localhost:8000/images/images/d.jpg"}


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
        user_id: int,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if user := await user_service.get_user_by_id(session, user_id):
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.get("/profile", response_model=UserOut)
async def profile(
        auth: User = Depends(utils.get_current_active_auth_user)
):
    return auth


@router.patch("/update-profile", response_model=UserOut)
async def update_profile(
        user_update: UserUpdatePartial,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await utils.convert_params_user(user_update)
    return user_service.update_user(session, auth, user_update)


@router.patch("/update-avatar", response_model=UserOut)
async def update_avatar(
        image: bytes,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    with open(path_to_avatar := f"app/images/avatars/{auth.id}.jpg", "wb") as file:
        file.write(image)

    return await user_service.update_user_avatar(session, auth, path_to_avatar)


@router.delete("/delete-avatar", response_model=UserOut)
async def delete_avatar(
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await user_service.delete_user_avatar(session, auth)


@router.post("/add-new-user", response_model=UserOut)
async def add_user(
        phone_number: str,
        user_add: UserRegistration,
        auth: User = Depends(utils.get_current_verified_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await utils.checking_registered(session, phone_number)
    await utils.convert_params_user(user_add)
    user = await user_service.create_user(session, phone_number)

    return await user_service.update_user(session, user, user_add)
