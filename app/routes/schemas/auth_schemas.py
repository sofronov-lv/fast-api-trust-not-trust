from random import randrange
from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field


def generate_code() -> str:
    return str(randrange(1000, 9999))


def get_date_update() -> datetime:
    return datetime.utcnow() + timedelta(minutes=1)


def get_date_life() -> datetime:
    return datetime.utcnow() + timedelta(minutes=10)


class PhoneNumberBase(BaseModel):
    country_code: int
    number: int


class OtcBase(BaseModel):
    phone_number: str


class CodeCreate(OtcBase):
    code: str = Field(default_factory=generate_code)
    date_update: datetime = Field(default_factory=get_date_update)
    date_life: datetime = Field(default_factory=get_date_life)
    attempts: int = 0
    approved: bool = False


class CodeUpdate(CodeCreate):
    model_config = ConfigDict(from_attributes=True)
    pass


class CodeOut(OtcBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_creation: datetime
    date_update: datetime
    date_life: datetime
    attempts: int


class TokenBase(BaseModel):
    token_type: str = "Bearer"


class AccessToken(TokenBase):
    access_token: str


class RefreshToken(TokenBase):
    refresh_token: str


class AuthInfo(AccessToken, RefreshToken):
    is_admin: bool
    is_active: bool
    is_registered: bool
