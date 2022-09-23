import factory
from faker import Factory as FakerFactory

from app.models.user import User
from app.db.session import SessionLocal
from app.core.security import get_password_hash

faker = FakerFactory.create()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    first_name = factory.LazyAttribute(lambda x: faker.name())
    surname = factory.LazyAttribute(lambda x: faker.name())
    email = factory.Sequence(lambda a: 'person_{}@example.com'.format(a).lower())
    is_superuser = False
    hashed_password = get_password_hash(faker.password())
