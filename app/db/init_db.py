import logging
from sqlalchemy.orm import Session
from core.security import get_password_hash

import crud
import schemas
from db import base  # noqa: F401
from core.settings import settings
from models.user import User

logger = logging.getLogger(__name__)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        # user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.FIRST_SUPERUSER_PW,
            )
            create_data = user_in.dict()
            create_data.pop("password")
            db_obj = User(**create_data)
            db_obj.hashed_password = get_password_hash(user_in.password)
            db.add(db_obj)
            db.commit()
            # user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
