import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class User(Base):
    __tablename__ = "users"

    path_to_avatar: Mapped[str] = mapped_column(default="app/images/DEFAULT.jpg")

    phone_number: Mapped[str] = mapped_column(unique=True)

    surname: Mapped[str | None]
    name: Mapped[str | None]
    patronymic: Mapped[str | None]
    fullname: Mapped[str | None]

    birthdate: Mapped[datetime.date | None]
    country: Mapped[str | None]
    city: Mapped[str | None]

    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    positive_scores: Mapped[int] = mapped_column(default=0)
    negative_scores: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float] = mapped_column(default=0.0)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_registered: Mapped[bool] = mapped_column(default=False)
