
from sqlalchemy.orm import Session

from app.controller.base import BaseController
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class AdminController(BaseController[User, UserCreate, UserUpdate]):
    ...


admin = AdminController(User)
