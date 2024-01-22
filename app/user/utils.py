import datetime


def convert_str_to_date(str_date: str) -> datetime.date:
    return datetime.datetime.strptime(str_date, "%d.%m.%y").date()
