import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    pass


class UserDeleteAvatar(UserBase):
    pass


class UserCreate(UserBase):
    phone_number: str


class UserUpdatePartial(UserBase):
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    birthdate: str | None = None
    country: str | None = None
    city: str | None = None


class UserLogin(UserBase):
    phone_number: str
    code: str


class UserRegistration(UserBase):
    surname: str
    name: str
    patronymic: str | None = None
    birthdate: str | datetime.date
    country: str
    city: str


class UserContactList(UserBase):
    phone_numbers: list[str]
    offset: int = 0
    limit: int = 10


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone_number: str
    path_to_avatar: str
    surname: str | None
    name: str | None
    patronymic: str | None = None
    fullname: str
    birthdate: str | None
    country: str | None
    city: str | None
    likes: int
    dislikes: int
    positive_scores: int
    negative_scores: int
    rating: float
    is_active: bool
    is_verified: bool
    is_registered: bool
