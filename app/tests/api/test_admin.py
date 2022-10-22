from app.core.settings import settings
from app.schemas.base import UserRole
from app.tests import UserFactory, generate_token, get_random_string
from app.core.security import get_password_hash


def test_fetch_all_users(client):
    UserFactory(hashed_password=get_password_hash(get_random_string()))
    UserFactory(hashed_password=get_password_hash(get_random_string()))
    UserFactory(hashed_password=get_password_hash(get_random_string()))

    user = UserFactory(hashed_password=get_password_hash(get_random_string()), is_superuser=True, role=UserRole.ADMIN)
    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }
    response = client.get(f"{settings.API_V1_STR}/admin/users", headers=header)
    data = response.json()

    assert response.status_code == 200
    assert len(data['data']) > 2


def test_does_not_fetch_all_users_for_non_superuser(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }
    response = client.get(f"{settings.API_V1_STR}/admin/users", headers=header)

    assert response.status_code == 401


def test_does_not_fetch_all_users_for_unauthenticated(client):
    UserFactory(hashed_password=get_password_hash(get_random_string()))

    response = client.get(f"{settings.API_V1_STR}/admin/users")

    assert response.status_code == 401


def test_fetch_user_by_id(client):
    user_1 = UserFactory(hashed_password=get_password_hash(get_random_string()))
    user_2 = UserFactory(hashed_password=get_password_hash(get_random_string()))

    admin_user = UserFactory(hashed_password=get_password_hash(
        get_random_string()), is_superuser=True, role=UserRole.ADMIN)
    token = generate_token(admin_user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }
    response = client.get(f"{settings.API_V1_STR}/admin/user/{user_1.id}", headers=header)
    user = response.json()

    assert response.status_code == 200
    assert user['data']['email'] == user_1.email
    assert user['data']['id'] != user_2.id


def test_delete_user_by_id(client, session):
    user_1 = UserFactory(hashed_password=get_password_hash(get_random_string()))
    user_2 = UserFactory(hashed_password=get_password_hash(get_random_string()))

    admin_user = UserFactory(hashed_password=get_password_hash(
        get_random_string()), is_superuser=True, role=UserRole.ADMIN)
    token = generate_token(admin_user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }

    response = client.delete(f"{settings.API_V1_STR}/admin/user/{user_1.id}", headers=header)

    assert response.status_code == 204

    from app.models.user import User
    deleted_user = session.query(User).filter(User.email == user_1.email).first()

    assert deleted_user == None

    second_user = session.query(User).filter(User.email == user_2.email).first()

    assert second_user.id == user_2.id
