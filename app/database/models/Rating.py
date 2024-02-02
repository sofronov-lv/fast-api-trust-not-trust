import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class Rating(Base):
    __tablename__ = "ratings"

    evaluator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    feedback: Mapped[bool]  # True - positive; False - negative
    score: Mapped[int]
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
