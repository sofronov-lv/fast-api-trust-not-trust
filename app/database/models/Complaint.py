import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class Complaint(Base):
    __tablename__ = "complaints"

    complaining_user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id", ondelete="CASCADE"))
    date: Mapped[datetime.date | None]
    reason: Mapped[str] = mapped_column(String(length=255))
    is_reviewed: Mapped[bool] = mapped_column(default=False, server_default="false")
