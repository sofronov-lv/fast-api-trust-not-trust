from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:2804@localhost:5432/asyncalchemy"
    db_echo: bool = False  # TODO: False


setting = Setting()
