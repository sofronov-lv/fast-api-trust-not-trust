import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Rating, Complaint

from app.routes.schemas.rating_schemas import RatingCreate, RatingUpdate, RatingBase, RatingSearch, ComplaintCreate, \
    ComplaintSearch
from app.routes.schemas.user_schemas import UsersSelection


async def get_rating(session: AsyncSession, rating_in: RatingSearch | RatingCreate) -> Rating | None:
    stmt = (
        select(Rating).
        where(Rating.user_id == rating_in.user_id).
        where(Rating.evaluator_id == rating_in.evaluator_id)
    )
    result = await session.execute(stmt)
    rating = result.scalars().one_or_none()
    return rating


async def get_ratings(session: AsyncSession, rating_in: RatingBase, selection: UsersSelection) -> list[Rating]:
    stmt = (
        select(Rating)
        .order_by(Rating.evaluator_id)
        .where(Rating.user_id == rating_in.user_id)
        .offset(selection.offset)
        .limit(selection.limit)
    )
    result = await session.execute(stmt)
    ratings = result.scalars().all()
    return list(ratings)


async def create_rating(session: AsyncSession, rating_create: RatingCreate) -> Rating:
    rating = Rating(
        **rating_create.model_dump(),
        date=datetime.datetime.utcnow()
    )
    session.add(rating)
    await session.commit()
    await session.refresh(rating)
    return rating


async def update_rating(session: AsyncSession, rating: Rating, rating_update: RatingUpdate | RatingCreate) -> Rating:
    rating.date = datetime.datetime.utcnow()
    for name, value in rating_update.model_dump(exclude_none=True).items():
        setattr(rating, name, value)

    await session.commit()
    return rating


async def create_complaint(session: AsyncSession, complaint_create: ComplaintCreate, user_id: int) -> Complaint:
    complaint = Complaint(
        **complaint_create.model_dump(),
        complaining_user_id=user_id,
        date=datetime.datetime.utcnow()
    )
    session.add(complaint)
    await session.commit()
    await session.refresh(complaint)
    return complaint


async def get_complaints_about_user(session: AsyncSession, user_id: int) -> Complaint | None:
    stmt = (
        select(Complaint)
        .where(Complaint.user_id == user_id)
        .where(Complaint.is_reviewed.is_(False))
    )
    result = await session.execute(stmt)
    complaint = result.scalars().first()
    return complaint


async def get_complaint(session: AsyncSession, complaint_in: ComplaintSearch) -> Complaint | None:
    stmt = (
        select(Complaint)
        .where(Complaint.user_id == complaint_in.user_id)
        .where(Complaint.complaining_user_id == complaint_in.complaining_user_id)
        .where(Complaint.is_reviewed.is_(False))
    )
    result = await session.execute(stmt)
    complaint = result.scalars().one_or_none()
    return complaint


async def get_complaints(session: AsyncSession, selection: UsersSelection) -> list[Complaint]:
    stmt = (
        select(Complaint)
        .order_by(Complaint.id)
        .where(Complaint.is_reviewed.is_(False))
        .offset(selection.offset)
        .limit(selection.limit)
    )
    result = await session.execute(stmt)
    complaints = result.scalars().all()
    return list(complaints)


async def deactivate_complaints_about_blocked_user(session: AsyncSession, user_id: int) -> None:
    stmt = (
        update(Complaint)
        .where(Complaint.user_id == user_id)
        .values(is_reviewed=False)
    )
    await session.execute(stmt)
    await session.commit()


async def update_review(session: AsyncSession, complaint_in: Complaint) -> Complaint:
    complaint_in.is_reviewed = True
    await session.commit()
    return complaint_in
