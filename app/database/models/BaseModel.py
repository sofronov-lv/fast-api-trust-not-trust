from peewee import *

from app.database.connection_db import db


class BaseModel(Model):
    class Meta:
        order_by = id
        database = db
