from app.core.settings import settings
from app.tests import UserFactory
from app.core.security import get_password_hash


def test_register_user(client):
    # When
    response = client.post(f"{settings.API_V1_STR}/auth/register",
                           json={"first_name": "Oyin", "surname": "S", "email": "oyins@example.com",
                                 "password": "password1", "is_superuser": False})
    data = response.json()

    # Then
    assert response.status_code == 201
    for key in data.keys():
        assert key in ["access_token", "token_type", "success", "data"]


def test_user_login(client):
    password = "p@ssword1"
    user = UserFactory(hashed_password=get_password_hash(password))
    assert user
    response = client.post(f"{settings.API_V1_STR}/auth/login",
                           data={"username": user.email, "password": password}
                           )

    data = response.json()
    assert response.status_code == 200
    for key in data.keys():
        assert key in ["access_token", "token_type"]
