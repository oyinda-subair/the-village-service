import json
from urllib import response
from app import crud
from app.core.settings import settings
from app.schemas.user import UserCreate


def test_create_user(client):
    # When
    response = client.post(f"{settings.API_V1_STR}/users/signup",
                           json={"first_name": "Oyin", "surname": "S", "email": "oyins@example.com",
                                 "password": "password1", "is_superuser": False})
    data = response.json()

    # Then
    assert response.status_code == 201
    for key in data.keys():
        assert key in ["id", "first_name", "surname", "email", "is_superuser"]


def test_user_login(client, session):
    user_create = UserCreate(first_name="Oyinda", surname="S", email="oyinda@example.com",
                             password="password1", is_superuser=False)
    user_data = crud.user.create(
        db=session,
        obj_in=user_create)
    response = client.post(f"{settings.API_V1_STR}/users/login",
                           data={"username": user_data.email, "password": "password1"}
                           )

    data = response.json()
    assert response.status_code == 200
    for key in data.keys():
        assert key in ["access_token", "token_type"]
