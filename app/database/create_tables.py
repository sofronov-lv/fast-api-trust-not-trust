from app.database.connection_db import db

from app.database.models.Users import User
from app.database.models.OneTimeCodes import OneTimeCode
from app.database.models.UserStatistics import UserStatistic
from app.database.models.UserRatings import UserRating


tables = [User, OneTimeCode, UserStatistic, UserRating]


def create_tables():
    with db:
        db.create_tables(tables)


def delete_tables():
    with db:
        db.drop_tables(tables)


if __name__ == "__main__":
    delete_tables()
    create_tables()
