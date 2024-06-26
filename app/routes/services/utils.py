from PIL import Image

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import db_helper
from app.database.models import Complaint
from app.database.models import User
from app.routes.schemas.auth_schemas import PhoneNumberBase

from app.routes.services import user_service
from app.routes.services import rating_service

from app.routes.schemas.user_schemas import UserUpdatePartial, UserRegistration, UserSearch
from app.routes.schemas.rating_schemas import ComplaintSearch

from app.utils import jwt_token
from app.utils.sms_api import send_sms

http_bearer = HTTPBearer()


async def verifying_phone_number(phone: PhoneNumberBase):
    return f"+{phone.country_code}{phone.number}"


async def checking_registered(
        phone_number: str = Depends(verifying_phone_number),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if await user_service.get_user_by_phone_number(session, phone_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user already exists"
        )
    return phone_number


def check_sms(phone_number: str, text: str, id_: int):
    if not send_sms(phone_number, text, id_):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to send sms"
        )


async def token_verification(cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> dict:
    access_token = cred.credentials
    try:
        return jwt_token.decode_jwt_access(access_token)
    except jwt_token.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Token error: {e}"
        )


async def get_current_auth_user(
        payload: dict = Depends(token_verification),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user_id: int | None = payload.get("sub")
    if user := await user_service.get_user_by_id(session, user_id):
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Token invalid"
    )


async def get_current_active_auth_user(user: User = Depends(get_current_auth_user)) -> User:
    if user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive"
    )


async def get_current_verified_user(user: User = Depends(get_current_active_auth_user)) -> User:
    if user.is_verified:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user must be verified"
    )


async def get_current_admin_user(user: User = Depends(get_current_active_auth_user)) -> User:
    if user.is_admin:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user must be admin"
    )


def get_access_token(user_id: int):
    access_token = jwt_token.encode_jwt_access(
        payload=jwt_token.generate_payload_access(user_id)
    )
    return access_token


def get_refresh_token(user_id: int):
    refresh_token = jwt_token.encode_jwt_refresh(
        payload=jwt_token.generate_payload_refresh(user_id)
    )
    return refresh_token


def refresh_access_token(cred: HTTPAuthorizationCredentials = Depends(http_bearer)):
    refresh_token = cred.credentials
    try:
        payload = jwt_token.decode_jwt_refresh(refresh_token)
        return jwt_token.encode_jwt_access(payload)
    except jwt_token.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Token error: {e}"
        )


async def format_title_for_str(user_update: UserUpdatePartial | UserRegistration | UserSearch):
    for name, value in user_update.model_dump().items():
        if str == type(value):
            value = value.title()
        setattr(user_update, name, value)

    return user_update


async def convert_params_user(user_update: UserUpdatePartial | UserRegistration | UserSearch):
    try:
        if user_update.birthdate:
            user_update.birthdate = user_service.convert_str_to_date(user_update.birthdate)
        user_update = await format_title_for_str(user_update)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The birthday parameter was passed incorrectly"
        )
    return user_update


async def checking_user(session: AsyncSession, user_id: int):
    if user := await user_service.get_user_by_id(session, user_id):
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


def is_image(file):
    try:
        img = Image.open(file.file)
        img.verify()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File is not image"
        )
