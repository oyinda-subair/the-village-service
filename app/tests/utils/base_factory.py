import factory
from faker import Factory as FakerFactory

from app.db.session import SessionLocal

faker = FakerFactory.create()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = 'commit'
