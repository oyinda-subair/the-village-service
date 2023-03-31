from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from loguru import logger

from app.core.settings import settings, ENV


connection_uri = settings.db.SQLALCHEMY_DATABASE_URI

if ENV == "Testing":
    connection_uri = settings.db.TEST_SQLALCHEMY_DATABASE_URL

if connection_uri.startswith("postgres://"):
    connection_uri = connection_uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    connection_uri,
    pool_pre_ping=True
)

if not database_exists(engine.url):
    logger.info("Creating Database")
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
