import datetime

from pydantic import BaseModel, ConfigDict


class CodeBase(BaseModel):
    phone_number: str


class CodeCreate(CodeBase):
    pass


class CodeInput(CodeBase):
    code: str


class CodeOut(CodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    date_creation: datetime.datetime
    date_update: datetime.datetime
    date_life: datetime.datetime
    attempts: int
    approved: bool
