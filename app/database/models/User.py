import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class User(Base):
    __tablename__ = "users"

    file_name: Mapped[str] = mapped_column(default="DEFAULT", server_default="DEFAULT")

    phone_number: Mapped[str] = mapped_column(unique=True)

    surname: Mapped[str | None]
    name: Mapped[str | None]
    patronymic: Mapped[str | None]
    fullname: Mapped[str | None]

    birthdate: Mapped[datetime.date | None]
    country: Mapped[str | None]
    region: Mapped[str | None]

    likes: Mapped[int] = mapped_column(default=0, server_default="0")
    dislikes: Mapped[int] = mapped_column(default=0, server_default="0")
    positive_scores: Mapped[int] = mapped_column(default=0, server_default="0")
    negative_scores: Mapped[int] = mapped_column(default=0, server_default="0")
    rating: Mapped[float] = mapped_column(default=0.0, server_default="0.0")

    is_admin: Mapped[bool] = mapped_column(default=False, server_default="false")
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    is_verified: Mapped[bool] = mapped_column(default=False, server_default="false")
    is_registered: Mapped[bool] = mapped_column(default=False, server_default="false")
