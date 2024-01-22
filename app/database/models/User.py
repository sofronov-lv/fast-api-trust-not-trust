import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class User(Base):
    __tablename__ = "users"

    path_to_avatar: Mapped[str] = mapped_column(default="app/images/DEFAULT.jpg")

    phone_number: Mapped[str] = mapped_column(unique=True)

    surname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str | None]
    full_name: Mapped[str | None]

    birthdate: Mapped[datetime.date]
    country: Mapped[str]
    city: Mapped[str]

    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    positive_scores: Mapped[int] = mapped_column(default=0)
    negative_scores: Mapped[int] = mapped_column(default=0)

    approved: Mapped[bool] = mapped_column(default=False)


# @staticmethod
# def get_statistics(id_=None):
#     if id_ is None:
#         return UserStatistic.create()
#     return UserStatistic.select().where(UserStatistic.id == id_).get()
#
# def calculate_rating(self):
#     if self.positive_scores + self.negative_scores <= 0:
#         return 0
#     return round(5 * self.positive_scores / (self.positive_scores + self.negative_scores), 1)
#
# def update_statistics(self, params: dict, old_feedback=None, old_score=None):
#     if old_feedback is not None:
#         if old_feedback:
#             self.likes -= 1
#             self.positive_scores -= old_score
#         else:
#             self.dislikes -= 1
#             self.negative_scores -= old_score
#
#     if params["feedback"]:
#         self.likes += 1
#         self.positive_scores += params["score"]
#     else:
#         self.dislikes += 1
#         self.negative_scores += params["score"]
#
#     self.save()
#
# class Meta:
#     db_table = "user_statistics"

# def get_info(self):
#     return {
#         "id": self.id,
#         "image_to_bytes": self.get_avatar(),
#         "phone_number": self.phone_number,
#
#         "surname": self.surname,
#         "name": self.name,
#         "patronymic": self.patronymic,
#         "full_name": self.full_name,
#         "birthdate": self.birthdate.strftime("%d.%m.%y"),
#
#         "country": self.country,
#         "city": self.city,
#         "approved": self.approved,
#
#         "statistic_id": self.statistic_id.id,
#         "likes": self.statistics_id.likes,
#         "dislikes": self.statistics_id.dislikes,
#         "rating": self.statistics_id.calculate_rating()
#     }
#
# def get_avatar(self):
#     return b64encode(open(f"{self.path_to_avatar}", "rb").read()).decode("utf-8")
#
# def update_avatar(self, image_to_bytes: bytes):
#     self.path_to_avatar = f"avatars/{self.id}.jpg"
#     self.save()
#
#     with open(f"{self.path_to_avatar}", "wb") as file:
#         file.write(image_to_bytes)
#
# def update_user_data(self, params: dict):
#     if params["phone_number"]:
#         self.phone_number = params["phone_number"]
#     if params["surname"]:
#         self.surname = params["surname"]
#     if params["name"]:
#         self.name = params["name"]
#     if params["patronymic"]:
#         self.patronymic = params["patronymic"]
#     if params["birthdate"]:
#         self.birthdate = params["birthdate"]
#     if params["country"]:
#         self.country = params["country"]
#     if params["city"]:
#         self.city = params["city"]
#
#     self.full_name = self.get_full_name({"surname": self.surname, "name": self.name, "patronymic": self.patronymic})
#     if not self.check_full_name(self.full_name):
#         return False
#
#     self.save()
#     return True
#
# @staticmethod
# def create_user(params: dict):
#     return User.create(
#         statistic_id=UserStatistic.get_statistic().id,
#         phone_number=params["phone_number"],
#         surname=params["surname"],
#         name=params["name"],
#         patronymic=params["patronymic"],
#         full_name=params["full_name"],
#         birthdate=params["birthdate"],
#         country=params["country"],
#         city=params["city"]
#     )
#
# @staticmethod
# def get_user(user_id=None, phone_number=""):
#     try:
#         if user_id:
#             return User.select().where(User.id == user_id).get()
#         return User.select().where(User.phone_number == phone_number).get()
#     except DoesNotExist:
#         return None
#
# @staticmethod
# def get_params(parser):
#     parser.add_argument("phone_number", type=str, help="Phone number cannot be blank", required=True)
#     parser.add_argument("surname", type=str, help="Surname cannot be blank", required=True)
#     parser.add_argument("name", type=str, help="Name cannot be blank", required=True)
#     parser.add_argument("patronymic", type=str, help="Patronymic cannot be blank", default="")
#     parser.add_argument("birthdate", type=str, help="Birthdate cannot be blank")
#     parser.add_argument("country", type=str, help="Country cannot be blank", required=True)
#     parser.add_argument("city", type=str, help="City cannot be blank", required=True)
#     return parser.parse_args()
#
# @staticmethod
# def get_format_phone_number(phone_number: str):
#     return "".join([x if x.isdigit() else "" for x in phone_number])
#
# @staticmethod
# def get_full_name(params: dict):
#     return f"{params['surname']} {params['name']} {params['patronymic']}".strip()
#
# @staticmethod
# def check_full_name(full_name: str):
#     """The full name must contain only alphabetic characters"""
#     return True if (full_name.replace(" ", "")).isalpha() else False
#
# @staticmethod
# def get_image_to_bytes(request):
#     return b64decode(request.json["image_to_bytes"])
#
# @staticmethod
# def remove_extra_spaces_from_all_parameters(params: dict) -> dict:
#     for key, value in params.items():
#         if type(value) == str:
#             params[key] = value.strip()
#     return params
#
# @staticmethod
# def get_birthdate(params: dict):
#     if not params["birthdate"]:
#         return None
#     try:
#         if len(params["birthdate"]) > len("dd.mm.yy"):
#             return datetime.strptime(params["birthdate"], "%d.%m.%Y").date()
#         else:
#             return datetime.strptime(params["birthdate"], "%d.%m.%y").date()
#     except ValueError:
#         return False
#
# class Meta:
#     db_table = "users"
