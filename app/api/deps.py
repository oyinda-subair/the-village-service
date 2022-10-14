from typing import Generator
from app import controller
from app.db.session import SessionLocal
from app.core.authentication import oauth2_scheme
from app.core.exception_handler import CustomException
from app.core.settings import settings
from app.models.user import User
from app.schemas.user import TokenData

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm.session import Session
from loguru import logger


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(user_id=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        logger.error("Deps(get_current_user): Could not validate credentials")
        raise credentials_exception
    return user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not controller.user.is_superuser(current_user):
        logger.error("Deps(get_current_active_superuser):  The user doesn't have enough privileges")
        raise CustomException(
            status.HTTP_403_FORBIDDEN, "The user doesn't have enough privileges"
        )
    return current_user
