import datetime

from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.User import User

from app.user.schemas import UserCreate, UserUpdatePartial, UserDeleteAvatar, UserContactList

from app.user import utils


async def get_users(session: AsyncSession, offset: int, limit: int) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt.offset(offset).limit(limit))
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    user = await session.get(User, user_id)
    return user


async def get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
    stmt = select(User).where(User.phone_number == phone_number)
    result: Result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return user


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user_in.birthdate = utils.convert_str_to_date(user_in.birthdate)
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, user: User, user_update: UserUpdatePartial) -> User:
    user_update.birthdate = utils.convert_str_to_date(user_update.birthdate)
    for name, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, name, value)

    await session.commit()
    return user


async def update_user_avatar(session: AsyncSession, user: User, path_to_avatar: str) -> User:
    user.path_to_avatar = path_to_avatar

    await session.commit()
    return user


async def delete_user_avatar(session: AsyncSession, user: User) -> User:
    user.path_to_avatar = "app/images/DEFAULT.jpg"

    await session.commit()
    return user


async def get_contact_list(session: AsyncSession, contacts: UserContactList) -> list[User]:
    stmt = select(User).where(User.phone_number.in_(contacts.phone_numbers))
    result: Result = await session.execute(stmt.offset(contacts.offset).limit(contacts.limit))
    users = result.scalars().all()
    return list(users)
