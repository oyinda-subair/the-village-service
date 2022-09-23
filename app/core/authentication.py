from datetime import datetime, timedelta
from typing import List, MutableMapping, Union, Any
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.settings import settings

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    payload["exp"] = expire

    payload["iat"] = datetime.utcnow()

    payload["sub"] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
