from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.routes.schemas.rating_schemas import ComplaintOut, ComplaintSearch
from app.routes.schemas.user_schemas import UsersSelection

from app.routes.services import user_service, utils, rating_service

from app.database.models import db_helper
from app.database.models import Complaint
from app.database.models import User

router = APIRouter(prefix="/api", tags=["Admin"])


@router.get("/block-user/{user_id}")
async def block_a_user(
        user_id: int,
        auth: User = Depends(utils.get_current_admin_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await utils.checking_user(session, user_id)
    await user_service.block_user(session, user)
    await rating_service.update_all_reviews_about_blocked_user(session, user_id)

    return JSONResponse(
        status_code=200,
        content={"message": "The user was blocked"}
    )


@router.post("/cancel-complaint/")
async def cancel_the_complaint(
        complaint_in: ComplaintSearch,
        auth: User = Depends(utils.get_current_admin_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    complaint = await rating_service.get_complaint(session, complaint_in)
    await rating_service.update_review(session, complaint)

    return JSONResponse(
        status_code=200,
        content={"message": "The complaint was successfully verified"}
    )


@router.post("/complaints/", response_model=list[ComplaintOut])
async def get_complaints(
        selection: UsersSelection,
        auth: User = Depends(utils.get_current_admin_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await rating_service.get_complaints(session, selection)
