import factory
from faker import Factory as FakerFactory

from app.db.session import SessionLocal
# from app.tests.utils.helper import TestingSessionLocal
from app.tests.utils.test_db import TestingSessionLocal

# faker = FakerFactory.create()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = TestingSessionLocal()
        sqlalchemy_session_persistence = 'commit'
