import datetime

from pydantic import BaseModel


class RatingBase(BaseModel):
    user_id: int


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
