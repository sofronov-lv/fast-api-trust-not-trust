from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.schemas.user_schemas import UserOut, UserContactList, UserSearch, UsersLimit, UserRatingOut
from app.routes.schemas.rating_schemas import RatingBase, RatingOut

from app.routes.services import user_service
from app.routes.services import rating_service

from app.database.models import db_helper
from app.database.models import User

from app.routes import utils

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.post("/", response_model=list[UserOut])
async def search_users(
        selection: UsersLimit,
        params: UserSearch,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await utils.convert_params_user(params)
    return await user_service.search_users_by_params(session, params, selection.offset, selection.limit)


@router.post("/{fullname}", response_model=list[UserOut])
async def search_users_by_fullname(
        fullname: str,
        selection: UsersLimit,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await user_service.search_users_by_fullname(session, fullname, selection.offset, selection.limit)


@router.post("/contacts", response_model=list[UserOut])
async def get_contacts(
        selection: UsersLimit,
        contacts: UserContactList,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await user_service.get_contact_list(session, contacts, selection.offset, selection.limit)


@router.post("/evaluators/", response_model=list[UserRatingOut])
async def get_evaluators(
        selection: UsersLimit,
        rating_in: RatingBase,
        auth: User = Depends(utils.get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await utils.checking_user(session, rating_in.user_id)
    ratings = await rating_service.get_ratings(session, rating_in, selection.offset, selection.limit)
    evaluators = [rating.evaluator_id for rating in ratings]

    users = await user_service.get_users_by_ids(session, evaluators)

    result = []
    for user, rating in zip(users, ratings):
        rating = rating.__dict__
        rating["rating_id"] = rating.pop("id")
        result.append(user.__dict__ | rating)

    return result
