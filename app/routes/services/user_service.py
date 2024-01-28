import datetime

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.routes.schemas.user_schemas import (
    UserUpdatePartial,
    UserContactList,
    UserRegistration
)


def convert_str_to_date(str_date: str) -> datetime.date:
    return datetime.datetime.strptime(str_date, "%d.%m.%y").date()


def get_fullname(surname: str, name: str, patronymic: str) -> str:
    if patronymic:
        return f"{surname} {name} {patronymic}".title()
    return f"{surname} {name}".title()


async def get_users(session: AsyncSession, offset: int, limit: int) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt.offset(offset).limit(limit))
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    user = await session.get(User, user_id)
    return user


async def get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
    stmt = select(User).where(User.phone_number == phone_number)
    result: Result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return user


async def create_user(session: AsyncSession, phone_number: str) -> User:
    user = User(phone_number=phone_number)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
        session: AsyncSession,
        user: User,
        user_update: UserUpdatePartial | UserRegistration,
        is_registration: bool = False
) -> User:
    for name, value in user_update.model_dump(exclude_unset=True).items():
        if str == type(value):
            value = value.title()
        setattr(user, name, value)

    user.is_registered = is_registration
    user.fullname = get_fullname(user.surname, user.name, user.patronymic)

    await session.commit()
    return user


async def update_user_avatar(session: AsyncSession, user: User, path_to_avatar: str) -> User:
    user.path_to_avatar = Path(path_to_avatar)
    await session.commit()
    return user


async def delete_user_avatar(session: AsyncSession, user: User) -> User:
    user.path_to_avatar = Path("app/images/DEFAULT.jpg")
    await session.commit()
    return user


async def get_contact_list(session: AsyncSession, contacts: UserContactList) -> list[User]:
    stmt = select(User).where(User.phone_number.in_(contacts.phone_numbers))
    result: Result = await session.execute(stmt.offset(contacts.offset).limit(contacts.limit))
    users = result.scalars().all()
    return list(users)
