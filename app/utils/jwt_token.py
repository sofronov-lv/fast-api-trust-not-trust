import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta

from app.core.config import setting


def generate_payload_access(user_id: int, now: datetime = datetime.utcnow()) -> dict:
    return {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(minutes=15)
    }


def generate_payload_refresh(user_id: int, now: datetime = datetime.utcnow()) -> dict:
    return {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(days=30)
    }


def encode_jwt_refresh(
        payload: dict,
        private_key: str = setting.auth_jwt.refresh_private_key_path.read_text(),
        algorithm: str = setting.auth_jwt.algorithm
):
    return jwt.encode(payload, private_key, algorithm=algorithm)


def decode_jwt_refresh(
        token: str | bytes,
        public_key: str = setting.auth_jwt.refresh_public_key_path.read_text(),
        algorithm: str = setting.auth_jwt.algorithm
) -> dict:
    return jwt.decode(token, public_key, algorithms=[algorithm])


def encode_jwt_access(
        payload: dict,
        private_key: str = setting.auth_jwt.access_private_key_path.read_text(),
        algorithm: str = setting.auth_jwt.algorithm
):
    return jwt.encode(payload, private_key, algorithm=algorithm)


def decode_jwt_access(
        token: str | bytes,
        public_key: str = setting.auth_jwt.access_public_key_path.read_text(),
        algorithm: str = setting.auth_jwt.algorithm
) -> dict:
    return jwt.decode(token, public_key, algorithms=[algorithm])
