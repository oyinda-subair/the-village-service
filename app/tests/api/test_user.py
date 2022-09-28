from app import controller
from app.core.settings import settings
from app.schemas.user import UserCreate
from app.tests import UserFactory, generate_token
from app.core.security import get_password_hash


def test_create_user(client):
    # When
    response = client.post(f"{settings.API_V1_STR}/users/signup",
                           json={"first_name": "Oyin", "surname": "S", "email": "oyins@example.com",
                                 "password": "password1", "is_superuser": False})
    data = response.json()

    # Then
    assert response.status_code == 201
    for key in data.keys():
        assert key in ["id", "first_name", "surname", "email", "is_superuser", "created_at", "updated_at"]


def test_user_login(client, session):
    user_create = UserCreate(first_name="Oyinda", surname="S", email="oyinda@example.com",
                             password="password1", is_superuser=False)
    user_data = controller.user.create(
        db=session,
        obj_in=user_create)
    response = client.post(f"{settings.API_V1_STR}/users/login",
                           data={"username": user_data.email, "password": "password1"}
                           )

    data = response.json()
    assert response.status_code == 200
    for key in data.keys():
        assert key in ["access_token", "token_type"]


def test_current_user(client, session):
    password = "password1"
    user = UserFactory(hashed_password=get_password_hash(password))
    assert user

    data = generate_token(user)

    header = {
        'Authorization': 'Bearer {}'.format(data['access_token'])
    }

    response = client.get(f"{settings.API_V1_STR}/users/me", headers=header)
    result = response.json()

    assert response.status_code == 200
    assert result["first_name"] == user.first_name


def test_update_user(client):
    password = "password1"
    user = UserFactory(hashed_password=get_password_hash(password))
    assert user

    data = generate_token(user)

    header = {
        'Authorization': 'Bearer {}'.format(data['access_token'])
    }

    user_update = {"surname": "Test"}

    response = client.put(f"{settings.API_V1_STR}/users/{user.id}", json=user_update, headers=header)
    result = response.json()

    assert response.status_code == 200
    assert result["surname"] != user.surname
    assert result["surname"] == user_update["surname"]


def test_delete_user(client, session):
    password = "password1"
    user = UserFactory(hashed_password=get_password_hash(password))
    assert user

    data = generate_token(user)

    header = {
        'Authorization': 'Bearer {}'.format(data['access_token'])
    }

    response = client.delete(f"{settings.API_V1_STR}/users/{user.id}", headers=header)

    assert response.status_code == 204

    from app.models.user import User
    deleted_user = session.query(User).filter(User.email == user.email).first()

    assert deleted_user == None
