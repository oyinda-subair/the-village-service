import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


TEST_DATABASE_URL = os.environ.get("TEST_DB_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)
