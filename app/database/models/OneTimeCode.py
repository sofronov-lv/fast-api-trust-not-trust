import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class OneTimeCode(Base):
    __tablename__ = "one_time_codes"

    phone_number: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str]

    date_update: Mapped[datetime.datetime]
    date_life: Mapped[datetime.datetime]

    attempts: Mapped[int] = mapped_column(default=0)
    approved: Mapped[bool] = mapped_column(default=False)
