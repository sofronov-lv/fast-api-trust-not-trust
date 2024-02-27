from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import OneTimeCode

from app.routes.schemas.auth_schemas import CodeCreate, CodeUpdate


async def get_code(session: AsyncSession, phone_number: str) -> OneTimeCode | None:
    stmt = (
        select(OneTimeCode)
        .where(OneTimeCode.phone_number == phone_number)
    )
    result = await session.execute(stmt)
    return result.scalars().one_or_none()


async def create_code(session: AsyncSession, phone_number: str) -> OneTimeCode:
    code_create = CodeCreate(phone_number=phone_number)
    code = OneTimeCode(**code_create.model_dump())

    session.add(code)
    await session.commit()
    await session.refresh(code)
    return code


async def update_code_all(session: AsyncSession, code: OneTimeCode, phone_number: str) -> OneTimeCode:
    code_update = CodeUpdate(hone_number=phone_number)
    for name, value in code_update.model_dump().items():
        setattr(code, name, value)

    await session.commit()
    return code


async def update_code_attempt(session: AsyncSession, code: OneTimeCode) -> OneTimeCode:
    code.attempts += 1
    await session.commit()
    return code


async def approve_code(session: AsyncSession, code: OneTimeCode) -> OneTimeCode:
    code.approved = True
    await session.commit()
    return code
