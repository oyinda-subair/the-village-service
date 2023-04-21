from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from loguru import logger

from app.core.settings import settings, ENV


connection_uri = settings.db.DATABASE_URL

if ENV == "Test":
    connection_uri = settings.db.TEST_DATABASE_URL

if connection_uri.startswith("postgres://"):
    connection_uri = connection_uri.replace("postgres://", "postgresql://", 1)


engine = create_engine(
    connection_uri,
    pool_pre_ping=True
)

# Create test db if it does not exits
if ENV == "Test" and not database_exists(engine.url):
    logger.info("Creating Test Database")
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
