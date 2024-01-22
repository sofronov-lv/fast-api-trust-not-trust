from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.user import crud

from app.user.schemas import UserOut, UserCreate, UserUpdatePartial, UserContactList

from app.database.models import db_helper


router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/avatar")
async def get_avatar(
        # user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return {"status": "ok", "url": f"http://localhost:8000/images/images/d.jpg"}


@router.get("/", response_model=list[UserOut])
async def get_users(
        offset: int = 0,
        limit: int = 10,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_users(session, offset, limit)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if user := await crud.get_user(session, user_id):
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!"
    )


# @router.post("/", response_model=UserOut)
# async def registration(
#         user: UserCreate,
#         session: AsyncSession = Depends(db_helper.session_dependency)
# ):
#     return await crud.create_user(session, user)


@router.post("/", response_model=UserOut)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if await crud.get_user_by_phone_number(session, user.phone_number) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user already exists!"
        )

    return await crud.create_user(session, user)


@router.patch("/update-profile", response_model=UserOut)
async def update_profile(
        user_id: int,
        update_user: UserUpdatePartial,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await crud.get_user(session, user_id)

    return await crud.update_user(session, user, update_user)


@router.patch("/update-avatar", response_model=UserOut)
async def update_avatar(
        user_id: int,
        image: bytes,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await crud.get_user(session, user_id)

    with open(path_to_avatar := f"app/images/avatars/{user_id}.jpg", "wb") as file:
        file.write(image)

    return await crud.update_user_avatar(session, user, path_to_avatar)


@router.delete("/delete-avatar", response_model=UserOut)
async def delete_avatar(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await crud.get_user(session, user_id)

    return await crud.delete_user_avatar(session, user)


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
