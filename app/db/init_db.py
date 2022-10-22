import logging
from sqlalchemy.orm import Session
from app.schemas.user import UserRole

import controller
import schemas
from db import base  # noqa: F401
from app.core.settings import settings

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    if settings.db.FIRST_SUPERUSER:
        user = controller.user.get_by_email(db, email=settings.db.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=settings.db.FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.db.FIRST_SUPERUSER_PW,
                role=UserRole.admin,
            )
            user = controller.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.db.FIRST_SUPERUSER} already exists. "
            )
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.antoniaandgrace.com"
        )
