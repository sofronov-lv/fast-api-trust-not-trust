from peewee import *
from datetime import datetime

from app.database.models.BaseModel import BaseModel


class OneTimeCode(BaseModel):
    id = PrimaryKeyField()
    phone_number = TextField(unique=True)
    code = TextField()
    date = DateTimeField()
    attempts = IntegerField(default=1)
    approved = BooleanField(default=False)

    @staticmethod
    def get_otc(phone_number: str):
        try:
            return OneTimeCode.select().where(OneTimeCode.phone_number == phone_number).get()
        except DoesNotExist:
            return None

    @staticmethod
    def create_otc(phone_number: str, code: str, date: datetime):
        return OneTimeCode.create(phone_number=phone_number, code=code, date=date)

    def update_otc(self, code: str, date: datetime):
        self.code = code
        self.date = date
        self.attempts = 0
        self.approved = False
        self.save()

    def update_otc_approved(self):
        self.approved = True
        self.save()

    def increase_otc_attempts(self):
        self.attempts += 1
        self.save()

    class Meta:
        db_table = "one_time_codes"
