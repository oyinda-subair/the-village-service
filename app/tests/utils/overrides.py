from .test_db import TestingSessionLocal


def override_get_db():
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()
