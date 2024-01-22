import argparse
import datetime

from peewee import *

from app.database.models.Base import BaseModel
from app.database.models.User import User


class UserRating(BaseModel):
    id = PrimaryKeyField()
    id_of_evaluator = ForeignKeyField(User, backref="user_data")  # id of the user who evaluates
    id_user = ForeignKeyField(User, backref="user_data")  # id of the user being evaluated
    date = DateField(default=datetime.date.today())
    feedback = BooleanField()  # True - positive; False - negative
    score = IntegerField()  # from 1 to 3

    @staticmethod
    def get_params(parser):
        parser.add_argument("id_user", type=int, help="User ID cannot be blank", required=True)
        parser.add_argument("feedback", type=str2bool, default=False, help="Activate nice mode.")
        parser.add_argument("score", type=int, help="Score cannot be blank", required=True)
        return parser.parse_args()

    @staticmethod
    def get_rating(params: dict):
        try:
            rating = UserRating.select().where(
                UserRating.id_of_evaluator == params["id_of_evaluator"],
                UserRating.id_user == params["id_user"]
            ).get()

            rating.update_rating(params)

        except DoesNotExist:
            rating = UserRating.create(
                id_of_evaluator=params["id_of_evaluator"],
                id_user=params["id_user"],
                feedback=params["feedback"],
                score=params["score"]
            )
            rating.update_rating(params, new_rate=True)

        return rating

    def get_dict(self):
        return {
            "date": self.date.strftime("%d.%m.%y"),
            "feedback": self.feedback,
            "score": self.score,
        }

    def update_rating(self, params: dict, new_rate=False):
        user = User.select().where(User.id == self.id_user).get()

        if new_rate:
            user.statistics_id.update_statistics(params)
        else:
            user.statistics_id.update_statistics(params, self.feedback, self.score)
            self.date = datetime.date.today().strftime("%Y-%m-%d")
            self.feedback = params["feedback"]
            self.score = params["score"]
            self.save()
            
    class Meta:
        db_table = "user_rating"


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
