from typing import Any, Optional

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import controller
from app import schemas
from app.api import deps
from app.core.authentication import create_access_token
from app.core.init_logger import logger
from app.core.security import verify_password
from app.core.exception_handler import CustomException
from app.models.user import User
from app.schemas.common import DataResponse
from app.schemas.user import ShortUserResponse, Token, UserRegistrationToken
from loguru import logger

router = APIRouter()


@router.post("/register", response_model=UserRegistrationToken, status_code=201)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    try:
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            logger.error("The user with this email already exists in the system")
            raise CustomException(
                code=status.HTTP_409_CONFLICT,
                message="The user with this email already exists in the system",
            )
        user = controller.user.create(db=db, obj_in=user_in)
        data = ShortUserResponse(
            id=user.id,
            first_name=user.first_name,
            surname=user.surname,
            email=user.email,
            is_superuser=user.is_superuser,
            role=user.role
        )

        result = {
            "access_token": create_access_token(sub=user.id),
            "token_type": "bearer",
            **DataResponse(success=True, data=data).dict()
        }

        return result
    except Exception as e:
        logger.error(f"Internal Server Error #{e}")
        raise CustomException(code=500, message="Oop! An Error has occured")


@router.post("/login", response_model=Token)
def user_login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    try:
        user = authenticate(email=form_data.username, password=form_data.password, db=db)
        if not user:
            logger.error("Incorrect username or password 😬")
            raise CustomException(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password 😬")

        return {
            "access_token": create_access_token(sub=user.id),
            "token_type": "bearer",
        }
    except Exception as e:
        logger.error(f"Internal Server Error #{e}")
        raise CustomException(code=500, message="Oop! An Error has occured")


def authenticate(*, email: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
