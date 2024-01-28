import os

from pathlib import Path
from dotenv import load_dotenv

from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

IQ_SMS_LOGIN = os.getenv("IQ_SMS_LOGIN")
IQ_SMS_PASSWORD = os.getenv("IQ_SMS_PASSWORD")

DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")


KEY_PATH = Path("../app/core/certs")


class DbSettings(BaseSettings):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False


class AuthJWT(BaseModel):
    access_private_key_path: Path = KEY_PATH / "access_token_private.pem"
    access_public_key_path: Path = KEY_PATH / "access_token_public.pem"
    refresh_private_key_path: Path = KEY_PATH / "refresh_token_private.pem"
    refresh_public_key_path: Path = KEY_PATH / "refresh_token_public.pem"
    algorithm: str = "RS256"


class Setting(BaseSettings):
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


setting = Setting()
