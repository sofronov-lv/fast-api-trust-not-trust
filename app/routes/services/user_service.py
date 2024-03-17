import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.models import Rating

from app.routes.schemas.user_schemas import (
    UserUpdatePartial,
    UserContactList,
    UserRegistration,
    UserSearch,
    UsersLimit
)


def convert_str_to_date(str_date: str) -> datetime.date:
    return datetime.datetime.strptime(str_date, "%d.%m.%y").date()


def get_fullname(surname: str, name: str, patronymic: str) -> str:
    if patronymic:
        return f"{surname} {name} {patronymic}".title()
    return f"{surname} {name}".title()


def calc_rating(u: User):
    try:
        rating = 5 * u.positive_scores / (u.positive_scores + u.negative_scores)
        return round(rating, 1)
    except ZeroDivisionError:
        return 0.0


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    user = await session.get(User, user_id)
    return user


async def get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
    stmt = (
        select(User)
        .where(User.phone_number == phone_number)
        .where(User.is_active.is_(True))
    )
    result = await session.execute(stmt)
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
    for field, value in user_update.model_dump(exclude_none=True).items():
        setattr(user, field, value)

    user.fullname = get_fullname(user.surname, user.name, user.patronymic)
    if is_registration:
        user.is_registered = True

    await session.commit()
    return user


async def update_user_rating(session: AsyncSession, rating: Rating, user: User, multiplier: int) -> User:
    if rating.feedback:
        user.likes += 1 * multiplier
        user.positive_scores += rating.score * multiplier
    else:
        user.dislikes += 1 * multiplier
        user.negative_scores += rating.score * multiplier

    user.rating = calc_rating(user)

    await session.commit()
    return user


async def update_user_avatar(session: AsyncSession, user: User) -> User:
    user.file_name = str(user.id)
    await session.commit()
    return user


async def delete_user_avatar(session: AsyncSession, user: User) -> User:
    user.file_name = "DEFAULT"
    await session.commit()
    return user


async def block_user(session: AsyncSession, user: User) -> User:
    user.is_active = False
    await session.commit()
    return user


async def get_contact_list(session: AsyncSession, contacts: UserContactList, selection: UsersLimit) -> list[User]:
    stmt = (
        select(User)
        .where(User.phone_number.in_(contacts.phone_numbers))
        .where(User.is_active.is_(True))
        .offset(selection.offset)
        .limit(selection.limit)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_evaluators_by_ids(session: AsyncSession, ids: list[int]) -> list[User]:
    stmt = (
        select(User)
        .order_by(User.id)
        .where(User.id.in_(ids))
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def search_users_by_params(session: AsyncSession, params: UserSearch, selection: UsersLimit) -> list[User]:
    stmt = (
        select(User)
        .where(User.is_active.is_(True))
    )
    for field, value in params.model_dump(exclude_none=True).items():
        stmt = stmt.filter(getattr(User, field) == value)

    stmt = (
        stmt
        .order_by(User.id)
        .offset(selection.offset)
        .limit(selection.limit)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def search_users_by_fullname(session: AsyncSession, fullname: str, selection: UsersLimit) -> list[User]:
    stmt = (
        select(User)
        .order_by(User.id)
        .where(User.fullname.like(f"%{fullname.title()}%"))
        .where(User.is_active.is_(True))
        .offset(selection.offset)
        .limit(selection.limit)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)
