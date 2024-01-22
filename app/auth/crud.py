from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.OneTimeCode import OneTimeCode
from app.database.models.OneTimeCode import get_date_creation, get_date_update, get_date_life, generate_code

from app.auth.schemas import CodeCreate


async def get_code(session: AsyncSession, phone_number: str) -> OneTimeCode | None:
    stmt = select(OneTimeCode).where(OneTimeCode.phone_number == phone_number)
    result: Result = await session.execute(stmt)
    return result.scalars().one_or_none()


async def create_code(session: AsyncSession, phone_number: str) -> OneTimeCode:
    code = OneTimeCode(phone_number=phone_number)
    session.add(code)
    await session.commit()
    await session.refresh(code)
    return code


async def update_code_all(session: AsyncSession, code: OneTimeCode) -> OneTimeCode:
    code.code = generate_code()
    code.date_creation = get_date_creation()
    code.date_update = get_date_update()
    code.date_life = get_date_life()
    code.attempts = 0
    code.approved = False
    await session.commit()
    return code


async def update_code_attempt(session: AsyncSession, code: OneTimeCode) -> OneTimeCode:
    code.attempts += 1
    await session.commit()
    return code


async def update_code_approve(session: AsyncSession, code: OneTimeCode) -> OneTimeCode:
    code.approved = True
    await session.commit()
    return code

