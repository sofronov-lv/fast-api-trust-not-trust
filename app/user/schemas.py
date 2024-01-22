import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    phone_number: str
    surname: str
    name: str
    patronymic: str | None = None
    full_name: str | None = None
    birthdate: str | datetime.date
    country: str
    city: str


class UserUpdatePartial(BaseModel):
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    full_name: str | None = None
    birthdate: str | datetime.date | None = None
    country: str | None = None
    city: str | None = None


class UserDeleteAvatar(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class UserContactList(BaseModel):
    phone_numbers: list[str]
    offset: int = 0
    limit: int = 10


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    path_to_avatar: str
    likes: int
    dislikes: int
    positive_scores: int
    negative_scores: int
    approved: bool
