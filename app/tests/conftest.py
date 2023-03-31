from typing import Generator

import pytest
from pytest_factoryboy import register
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import close_all_sessions
from app.core.settings import settings, ENV

from app.main import app
from app.api import deps
from app.db.config import Base
from app.models.user import User
from app.tests.factories import CommentFactory, PostFactory, UserFactory
from app.tests.utils.overrides import override_get_db
from app.tests.utils.test_db import TestingSessionLocal, engine

settings.ENVIRONMENT = "test"
register(UserFactory)
register(PostFactory)
register(CommentFactory)


# @pytest.fixture(scope="session", autouse=True)
# def test_config(monkeypatch):
#     monkeypatch.setenv("ENVIRONMENT", "test")
# print(f"enviroment ***: {ENV}")

# @pytest.fixture()
# def session():
#     Base.metadata.create_all(bind=engine)
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = TestingSessionLocal(bind=connection)

#     # Begin a nested transaction (using SAVEPOINT).
#     nested = connection.begin_nested()

#     # If the application code calls session.commit, it will end the nested
#     # transaction. Need to start a new one when that happens.
#     @sa.event.listens_for(session, "after_transaction_end")
#     def end_savepoint(session, transaction):
#         nonlocal nested
#         if not nested.is_active:
#             nested = connection.begin_nested()

#     yield session

#     # Rollback the overall transaction, restoring the state before the test ran.
#     session.close()
#     transaction.rollback()
#     connection.close()


TEST_DB_NAME = "the_village_test"


@pytest.fixture(scope="session")
def connection(request):
    connection = engine.connect()
    return connection


@pytest.fixture(scope="session", autouse=True)
def setup_db(connection, request):
    """Setup test database.

    Creates all database tables as declared in SQLAlchemy models,
    then proceeds to drop all the created tables after all tests
    have finished running.
    """
    Base.metadata.bind = connection
    Base.metadata.create_all()

    def teardown():
        Base.metadata.drop_all()

    request.addfinalizer(teardown)


@pytest.fixture(autouse=True)
def session(connection, request):
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    session.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    def teardown():
        close_all_sessions()
        transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as test_client:
        # def override_get_db():
        #     yield session
        app.dependency_overrides[deps.get_db] = override_get_db
        yield test_client
        app.dependency_overrides = {}
