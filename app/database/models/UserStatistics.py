from peewee import *

from app.database.models.BaseModel import BaseModel


class UserStatistic(BaseModel):
    id = PrimaryKeyField()
    likes = IntegerField(default=0)
    dislikes = IntegerField(default=0)
    positive_scores = IntegerField(default=0)
    negative_scores = IntegerField(default=0)

    @staticmethod
    def get_statistics(id_=None):
        if id_ is None:
            return UserStatistic.create()
        return UserStatistic.select().where(UserStatistic.id == id_).get()

    def calculate_rating(self):
        if self.positive_scores + self.negative_scores <= 0:
            return 0
        return round(5 * self.positive_scores / (self.positive_scores + self.negative_scores), 1)

    def update_statistics(self, params: dict, old_feedback=None, old_score=None):
        if old_feedback is not None:
            if old_feedback:
                self.likes -= 1
                self.positive_scores -= old_score
            else:
                self.dislikes -= 1
                self.negative_scores -= old_score

        if params["feedback"]:
            self.likes += 1
            self.positive_scores += params["score"]
        else:
            self.dislikes += 1
            self.negative_scores += params["score"]

        self.save()

    class Meta:
        db_table = "user_statistics"
