from app.core.settings import settings
from app.tests import UserFactory, generate_token, PostFactory
from app.core.security import get_password_hash
from app.tests.utils.helper import get_random_string, get_random_sentence


def test_create_post(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }
    payload = {
        'title': get_random_sentence(),
        'content': '{} {}'.format(get_random_sentence(), get_random_sentence()),
        'category': 'Early Pregnancy',
        'image_url': 'http://{}-image.com'.format(get_random_string())
    }
    response = client.post(f"{settings.API_V1_STR}/posts/", json=payload, headers=header)
    data = response.json()

    assert response.status_code == 201
    assert len(data) > 0
    assert data['user_id'] == str(user.id)


def test_get_post(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    post = PostFactory(user=user)

    response = client.get(f"{settings.API_V1_STR}/posts/{post.id}")
    data = response.json()

    assert response.status_code == 200
    assert data['title'] == post.title


def test_get_my_posts(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    post1 = PostFactory(user=user)
    post2 = PostFactory(user=user)
    post3 = PostFactory()

    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }

    response = client.get(f"{settings.API_V1_STR}/posts/", headers=header)
    data = response.json()

    assert response.status_code == 200
    assert len(data) >= 3

    res = []
    user_ids = []

    for v in data['data']['posts']:
        res.append(v['id'])
        user_ids.append(v['user_id'])

    assert len(res) == 2
    assert sorted(res) == sorted([str(post1.id), str(post2.id)])
    assert str(post3.user_id) not in user_ids


def test_get_all_posts(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    PostFactory(user=user)
    PostFactory(user=user)
    post3 = PostFactory()

    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }

    response = client.get(f"{settings.API_V1_STR}/posts/all", headers=header)
    data = response.json()

    assert response.status_code == 200
    assert len(data) >= 3

    user_ids = []

    for v in data['data']['posts']:
        user_ids.append(v['user_id'])

    assert str(post3.user_id) in user_ids


def test_update_post(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    post_1 = PostFactory(user=user)
    post_2 = PostFactory()

    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }

    post_update = {"title": "Test"}

    response = client.put(f"{settings.API_V1_STR}/posts/{post_2.id}", json=post_update, headers=header)
    assert response.status_code == 403

    response = client.put(f"{settings.API_V1_STR}/posts/{post_1.id}", json=post_update, headers=header)
    data = response.json()

    assert response.status_code == 200
    assert data['title'] == post_update['title']


def test_delete_post(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    post_1 = PostFactory(user=user)
    post_2 = PostFactory()

    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }

    response = client.delete(f"{settings.API_V1_STR}/posts/{post_2.id}", headers=header)
    assert response.status_code == 403

    response = client.delete(f"{settings.API_V1_STR}/posts/{post_1.id}", headers=header)

    assert response.status_code == 204
