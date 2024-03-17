import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.schemas.auth_schemas import AuthInfo, AccessToken
from app.routes.schemas.user_schemas import UserOut, UserRegistration, UserLogin

from app.routes.services import user_service, utils
from app.routes.services import auth_service

from app.database.models import db_helper
from app.database.models import User


router = APIRouter(prefix="/api", tags=["Auth"])


@router.post("/code/")
async def get_one_time_code(
        phone_number: str = Depends(utils.verifying_phone_number),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if otc := await auth_service.get_code(session, phone_number):
        if otc.date_update > datetime.datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="You need to wait 1 minute before sending a new SMS message"
            )
        code = await auth_service.update_code_all(session, otc, phone_number)

    else:
        code = await auth_service.create_code(session, phone_number)

    utils.check_sms(phone_number, code.code, code.id)
    return JSONResponse(
        status_code=200,
        content={"message": "The code has been sent successfully"}
    )


async def validate_auth_user(
        login: UserLogin,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if (otc := await auth_service.get_code(session, login.phone_number)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this phone number was not found"
        )
    elif otc.approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The code has already been applied before"
        )
    elif otc.date_life < datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="The code's lifetime has expired"
        )
    elif otc.attempts > 2:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="The number of attempts to enter the code has been exceeded"
        )
    elif otc.code != login.code:
        await auth_service.update_code_attempt(session, otc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The code was entered incorrectly"
        )
    await auth_service.approve_code(session, otc)
    return login


async def verifying_auth_registered_user(
        login: UserLogin = Depends(validate_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if user := await user_service.get_user_by_phone_number(session, login.phone_number):
        return user
    return await user_service.create_user(session, login.phone_number)


@router.post("/login/", response_model=AuthInfo)
async def user_login(
        user: User = Depends(verifying_auth_registered_user)
):
    return AuthInfo(
        is_admin=user.is_admin,
        is_active=user.is_active,
        is_registered=user.is_registered,
        access_token=utils.get_access_token(user.id),
        refresh_token=utils.get_refresh_token(user.id),
        token_type="Bearer"
    )


async def verifying_auth_unregistered_user(
        auth: User = Depends(utils.get_current_active_auth_user)
):
    if auth.is_registered:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user is already registered"
        )
    return auth


@router.post("/registration/", response_model=UserOut)
async def registration(
        user_update: UserRegistration,
        auth: User = Depends(verifying_auth_unregistered_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user_update = await utils.convert_params_user(user_update)
    return await user_service.update_user(session, auth, user_update, is_registration=True)


@router.post("/refresh-token/", response_model=AccessToken)
async def refresh_access_token(
        new_access_token: str = Depends(utils.refresh_access_token)
):
    return AccessToken(access_token=new_access_token)
