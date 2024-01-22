import datetime
import random

from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


def get_date_creation() -> datetime.datetime:
    return datetime.datetime.now()


def get_date_update() -> datetime.datetime:
    return datetime.datetime.now() + datetime.timedelta(minutes=1)


def get_date_life() -> datetime.datetime:
    return datetime.datetime.now() + datetime.timedelta(minutes=10)


def generate_code() -> str:
    return str(random.randrange(1000, 9999))


class OneTimeCode(Base):
    __tablename__ = "one_time_codes"

    phone_number: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str] = mapped_column(default=generate_code())

    date_creation: Mapped[datetime.datetime] = mapped_column(default=get_date_creation())
    date_update: Mapped[datetime.datetime] = mapped_column(default=get_date_update())
    date_life: Mapped[datetime.datetime] = mapped_column(default=get_date_life())

    attempts: Mapped[int] = mapped_column(default=0)
    approved: Mapped[bool] = mapped_column(default=False)

    # @staticmethod
    # def get_otc(phone_number: str):
    #     try:
    #         return OneTimeCode.select().where(OneTimeCode.phone_number == phone_number).get()
    #     except DoesNotExist:
    #         return None
    #
    # @staticmethod
    # def create_otc(phone_number: str, code: str, date: datetime):
    #     return OneTimeCode.create(phone_number=phone_number, code=code, date=date)
    #
    # def update_otc(self, code: str, date: datetime):
    #     self.code = code
    #     self.date = date
    #     self.attempts = 0
    #     self.approved = False
    #     self.save()
    #
    # def update_otc_approved(self):
    #     self.approved = True
    #     self.save()
    #
    # def increase_otc_attempts(self):
    #     self.attempts += 1
    #     self.save()
    #
    # class Meta:
    #     db_table = "one_time_codes"
