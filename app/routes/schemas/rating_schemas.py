import datetime

from pydantic import BaseModel, constr


class RatingBase(BaseModel):
    user_id: int


class RatingSearch(RatingBase):
    evaluator_id: int


class RatingScore(RatingBase):
    feedback: bool
    score: int


class RatingCreate(RatingScore):
    evaluator_id: int = None


class RatingUpdate(RatingCreate):
    pass


class RatingOut(RatingCreate):
    id: int
    date: datetime.datetime


class ComplaintBase(BaseModel):
    pass


class ComplaintCreate(ComplaintBase):
    user_id: int
    reason: constr(max_length=255)


class ComplaintOut(ComplaintCreate):
    id: int
    complaining_user_id: int
    date: datetime.date | None
    is_reviewed: bool
