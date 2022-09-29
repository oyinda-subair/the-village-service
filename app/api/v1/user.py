from typing import Any, Optional
import uuid

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
from app.schemas.user import Token
from loguru import logger


router = APIRouter()


@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        logger.error("The user with this email already exists in the system")
        raise CustomException(
            code=status.HTTP_409_CONFLICT,
            message="The user with this email already exists in the system",
        )
    user = controller.user.create(db=db, obj_in=user_in)

    return user


@router.post("/login", response_model=Token)
def user_login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        logger.error("Incorrect username or password 😬")
        raise CustomException(status.HTTP_400_BAD_REQUEST, "Incorrect username or password 😬")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    user = current_user
    return user


@router.put("/{user_id}", response_model=schemas.User, status_code=200)
def user_update(
        *, db: Session = Depends(deps.get_db),
        user_id: str,
        user_in: schemas.UserUpdate, current_user: User = Depends(deps.get_current_user)) -> Any:
    user = _get_user(db, uuid.UUID(user_id), current_user.id)
    updated_user = controller.user.update(db=db, db_obj=user, obj_in=user_in)
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete_user(
        *, db: Session = Depends(deps.get_db),
        user_id: str, current_user: User = Depends(deps.get_current_user)) -> Any:
    _ = _get_user(db, uuid.UUID(user_id), current_user.id)
    return controller.user.delete(db=db, id=uuid.UUID(user_id))


def authenticate(*, email: str, password: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def _get_user(db: Session, id: uuid.UUID, current_user_id: uuid.UUID) -> Any:
    user = controller.user.get(db, id=current_user_id)
    if not user:
        logger.error(f"User with ID: {current_user_id} not found.")
        raise CustomException(
            status.HTTP_404_NOT_FOUND, f"User with ID: {current_user_id} not found."
        )

    if id != current_user_id:
        logger.error(f"You can only update your profile.")
        raise CustomException(
            status.HTTP_403_FORBIDDEN, f"You can only update your profile."
        )
    return user
