from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from loguru import logger

from app.core.settings import settings


connection_uri = settings.db.SQLALCHEMY_DATABASE_URI

if connection_uri.startswith("postgres://"):
    connection_uri = connection_uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    connection_uri,
)

if not settings.TEST_FLAG and not database_exists(engine.url):
    logger.info("Creating Database")
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
