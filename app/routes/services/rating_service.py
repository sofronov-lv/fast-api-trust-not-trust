import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Rating

from app.routes.schemas.rating_schemas import RatingCreate, RatingUpdate, RatingBase, RatingSearch


async def get_rating(
        session: AsyncSession,
        rating_in: RatingSearch | RatingCreate
) -> Rating | None:
    stmt = (
        select(Rating).
        where(Rating.user_id == rating_in.user_id).
        where(Rating.evaluator_id == rating_in.evaluator_id)
    )
    result = await session.execute(stmt)
    rating = result.scalars().one_or_none()
    return rating


async def get_ratings(
        session: AsyncSession,
        rating_in: RatingBase,
        offset: int,
        limit: int,
) -> list[Rating]:
    stmt = (
        select(Rating)
        .order_by(Rating.evaluator_id)
        .where(Rating.user_id == rating_in.user_id)
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    ratings = result.scalars().all()
    return list(ratings)


async def create_rating(session: AsyncSession, rating_create: RatingCreate) -> Rating:
    rating = Rating(**rating_create.model_dump(), date=datetime.datetime.utcnow())
    session.add(rating)
    await session.commit()
    await session.refresh(rating)
    return rating


async def update_rating(
        session: AsyncSession,
        rating: Rating,
        rating_update: RatingUpdate | RatingCreate
) -> Rating:
    rating.date = datetime.datetime.utcnow()
    for name, value in rating_update.model_dump(exclude_none=True).items():
        setattr(rating, name, value)

    await session.commit()
    return rating
