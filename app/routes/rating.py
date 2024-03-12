from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes import utils

from app.routes.schemas.rating_schemas import RatingOut, RatingCreate, RatingScore, RatingSearch
from app.routes.schemas.rating_schemas import ComplaintCreate, ComplaintOut

from app.routes.services import user_service
from app.routes.services import rating_service

from app.database.models import db_helper
from app.database.models import User

router = APIRouter(prefix="/api/rating", tags=["Rating"])


@router.get("/my-evaluation/{user_id}", response_model=RatingOut)
async def get_my_evaluation(
        user_id: int,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    rating_in = RatingSearch(user_id=user_id, evaluator_id=auth.id)
    if rating := await rating_service.get_rating(session, rating_in):
        return rating

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The record was not found"
    )


async def check_validity_params(
        rating: RatingScore,
        auth: User = Depends(utils.get_current_active_auth_user)
) -> RatingCreate:
    if rating.user_id == auth.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't evaluate yourself"
        )
    elif rating.score not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The glasses are graded from 1 to 3"
        )

    return RatingCreate(**rating.model_dump(), evaluator_id=auth.id)


@router.post("/rate/", response_model=RatingOut)
async def rate_user(
        rating_create: RatingCreate = Depends(check_validity_params),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await utils.checking_user(session, rating_create.user_id)

    if (rating := await rating_service.get_rating(session, rating_create)) is None:
        rating = await rating_service.create_rating(session, rating_create)
        await user_service.update_user_rating(session, rating, user, multiplier=1)
        return rating

    user = await user_service.update_user_rating(session, rating, user, multiplier=-1)
    new_rating = await rating_service.update_rating(session, rating, rating_create)
    await user_service.update_user_rating(session, new_rating, user, multiplier=1)

    return new_rating


@router.post("/complaint/", response_model=ComplaintOut)
async def complaint_about_the_user(
        complaint_create: ComplaintCreate,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await utils.checking_user(session, complaint_create.user_id)

    if await rating_service.get_complaint(session, complaint_create.user_id, auth.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The complaint has already been submitted for consideration"
        )
    return await rating_service.create_complaint(session, complaint_create, auth.id)
