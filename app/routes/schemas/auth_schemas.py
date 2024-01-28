from random import randrange
from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field


def generate_code() -> str:
    return str(randrange(1000, 9999))


def get_date_update() -> datetime:
    return datetime.utcnow() + timedelta(minutes=1)


def get_date_life() -> datetime:
    return datetime.utcnow() + timedelta(minutes=10)


class CodeBase(BaseModel):
    phone_number: str
    code: str


class CodeCreate(CodeBase):
    code: str = Field(default_factory=generate_code)
    date_update: datetime = Field(default_factory=get_date_update)
    date_life: datetime = Field(default_factory=get_date_life)
    attempts: int = 0
    approved: bool = False


class CodeUpdate(CodeCreate):
    model_config = ConfigDict(from_attributes=True)
    pass


class CodeOut(CodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_creation: datetime
    date_update: datetime
    date_life: datetime
    attempts: int


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenInfo(AccessToken):
    is_registered: bool
    refresh_token: str
