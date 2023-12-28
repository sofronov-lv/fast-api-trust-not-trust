from peewee import *
from datetime import datetime
from base64 import b64decode, b64encode

from app.database.models.BaseModel import BaseModel
from app.database.models.UserStatistics import UserStatistic


class User(BaseModel):
    id = PrimaryKeyField()
    statistic_id = ForeignKeyField(UserStatistic, backref="statistic", unique=True)

    path_to_avatar = TextField(default="avatars/DEFAULT.jpg")
    phone_number = TextField(unique=True)

    surname = TextField()
    name = TextField()
    patronymic = TextField(null=True)
    full_name = TextField()

    birthdate = DateField(null=True)

    country = TextField()
    city = TextField()
    approved = BooleanField(default=False)

    def get_info(self):
        return {
            "id": self.id,
            "image_to_bytes": self.get_avatar(),
            "phone_number": self.phone_number,

            "surname": self.surname,
            "name": self.name,
            "patronymic": self.patronymic,
            "full_name": self.full_name,
            "birthdate": self.birthdate.strftime("%d.%m.%y"),

            "country": self.country,
            "city": self.city,
            "approved": self.approved,

            "statistic_id": self.statistic_id.id,
            "likes": self.statistics_id.likes,
            "dislikes": self.statistics_id.dislikes,
            "rating": self.statistics_id.calculate_rating()
        }

    def get_avatar(self):
        return b64encode(open(f"{self.path_to_avatar}", "rb").read()).decode("utf-8")

    def update_avatar(self, image_to_bytes: bytes):
        self.path_to_avatar = f"avatars/{self.id}.jpg"
        self.save()

        with open(f"{self.path_to_avatar}", "wb") as file:
            file.write(image_to_bytes)

    def update_user_data(self, params: dict):
        if params["phone_number"]:
            self.phone_number = params["phone_number"]
        if params["surname"]:
            self.surname = params["surname"]
        if params["name"]:
            self.name = params["name"]
        if params["patronymic"]:
            self.patronymic = params["patronymic"]
        if params["birthdate"]:
            self.birthdate = params["birthdate"]
        if params["country"]:
            self.country = params["country"]
        if params["city"]:
            self.city = params["city"]

        self.full_name = self.get_full_name({"surname": self.surname, "name": self.name, "patronymic": self.patronymic})
        if not self.check_full_name(self.full_name):
            return False

        self.save()
        return True

    @staticmethod
    def create_user(params: dict):
        return User.create(
            statistic_id=UserStatistic.get_statistic().id,
            phone_number=params["phone_number"],
            surname=params["surname"],
            name=params["name"],
            patronymic=params["patronymic"],
            full_name=params["full_name"],
            birthdate=params["birthdate"],
            country=params["country"],
            city=params["city"]
        )

    @staticmethod
    def get_user(user_id=None, phone_number=""):
        try:
            if user_id:
                return User.select().where(User.id == user_id).get()
            return User.select().where(User.phone_number == phone_number).get()
        except DoesNotExist:
            return None

    @staticmethod
    def get_params(parser):
        parser.add_argument("phone_number", type=str, help="Phone number cannot be blank", required=True)
        parser.add_argument("surname", type=str, help="Surname cannot be blank", required=True)
        parser.add_argument("name", type=str, help="Name cannot be blank", required=True)
        parser.add_argument("patronymic", type=str, help="Patronymic cannot be blank", default="")
        parser.add_argument("birthdate", type=str, help="Birthdate cannot be blank")
        parser.add_argument("country", type=str, help="Country cannot be blank", required=True)
        parser.add_argument("city", type=str, help="City cannot be blank", required=True)
        return parser.parse_args()

    @staticmethod
    def get_format_phone_number(phone_number: str):
        return "".join([x if x.isdigit() else "" for x in phone_number])

    @staticmethod
    def get_full_name(params: dict):
        return f"{params['surname']} {params['name']} {params['patronymic']}".strip()

    @staticmethod
    def check_full_name(full_name: str):
        """The full name must contain only alphabetic characters"""
        return True if (full_name.replace(" ", "")).isalpha() else False

    @staticmethod
    def get_image_to_bytes(request):
        return b64decode(request.json["image_to_bytes"])

    @staticmethod
    def remove_extra_spaces_from_all_parameters(params: dict) -> dict:
        for key, value in params.items():
            if type(value) == str:
                params[key] = value.strip()
        return params

    @staticmethod
    def get_birthdate(params: dict):
        if not params["birthdate"]:
            return None
        try:
            if len(params["birthdate"]) > len("dd.mm.yy"):
                return datetime.strptime(params["birthdate"], "%d.%m.%Y").date()
            else:
                return datetime.strptime(params["birthdate"], "%d.%m.%y").date()
        except ValueError:
            return False

    class Meta:
        db_table = "users"
