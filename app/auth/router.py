import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import crud

from app.auth.schemas import CodeInput

from app.database.models import db_helper

from .sms_api import SMS


router = APIRouter(prefix="/api/code", tags=["Code"])


@router.get("/{phone_number}")
async def get_code(
        phone_number: str,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if (code := await crud.get_code(session, phone_number)) is None:
        code = await crud.create_code(session, phone_number)

    elif code.date_update > datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You need to wait 1 minute before sending a new SMS message"
        )

    else:
        code = await crud.update_code_all(session, code)

    # TODO: replace with commented-out lines
    print(code.code)
    return JSONResponse(status_code=200, content={"message": "The code has been sent successfully"})
    # if SMS.send_sms(phone_number, code.code, code.id):
    #     return JSONResponse(
    #         status_code=200,
    #         content={"message": "The code has been sent successfully"}
    #     )
    # raise HTTPException(
    #     status_code=status.HTTP_400_BAD_REQUEST,
    #     detail="Failed to send sms"
    # )


@router.post("/")
async def post_code(
        code_in: CodeInput,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if (code := await crud.get_code(session, code_in.phone_number)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this phone number was not found"
        )

    elif code.date_life < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="The code's lifetime has expired"
        )

    elif code.attempts > 2:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="The number of attempts to enter the code has been exceeded"
        )

    elif code.code != code_in.code:
        await crud.update_code_attempt(session, code)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The code was entered incorrectly"
        )

    elif code.code == code_in.code:
        await crud.update_code_approve(session, code)
        return JSONResponse(
            status_code=200,
            content={"message": "The code was successfully accepted"}
        )
