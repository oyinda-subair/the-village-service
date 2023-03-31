import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


TEST_SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_DATABASE_URI")

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)
