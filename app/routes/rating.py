from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes import utils

from app.routes.schemas.rating_schemas import RatingBase, RatingUpdate, RatingOut, RatingCreate, RatingScore

from app.routes.services import user_service
from app.routes.services import rating_service

from app.database.models import db_helper
from app.database.models import User
from app.database.models import Rating

router = APIRouter(prefix="/api/rating", tags=["Rating"])


@router.get("/", response_model=RatingOut)
async def get_rating(
        rating_in: RatingBase,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    if (rating := await rating_service.get_rating(session, rating_in)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The record was not found"
        )
    return rating


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


@router.post("/rate", response_model=RatingOut)
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
