from app.core.settings import settings
from app.tests import UserFactory, generate_token, PostFactory, CommentFactory
from app.core.security import get_password_hash
from app.tests.utils.helper import get_random_string, get_random_sentence


def test_create_comment(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    post = PostFactory(user=user)
    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }
    payload = {
        'content': '{} {}'.format(get_random_sentence(), get_random_sentence()),
    }
    post_id = str(post.id)
    response = client.post(f"{settings.API_V1_STR}/comments/?post_id={post_id}", json=payload, headers=header)
    data = response.json()

    assert response.status_code == 201
    assert len(data) > 0
    assert data['user_id'] == str(user.id)


def test_get_comments(client):
    post = PostFactory()
    for _ in range(10):
        CommentFactory(post=post)

    post_id = str(post.id)
    response = client.get(f"{settings.API_V1_STR}/comments/?post_id={post_id}&limit={5}&skip={0}")
    data = response.json()

    assert response.status_code == 200
    assert data["data"]["results"] == 5


def test_update_comment(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    comment_1 = CommentFactory(user=user)
    comment_2 = CommentFactory()

    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }

    comment_update = {"content": "Test"}

    response = client.put(f"{settings.API_V1_STR}/comments/{comment_2.id}", json=comment_update, headers=header)
    assert response.status_code == 403

    response = client.put(f"{settings.API_V1_STR}/comments/{comment_1.id}", json=comment_update, headers=header)
    data = response.json()

    assert response.status_code == 200
    assert data['content'] == comment_update['content']


def test_delete_comment(client):
    user = UserFactory(hashed_password=get_password_hash(get_random_string()))
    comment_1 = CommentFactory(user=user)
    comment_2 = CommentFactory()

    token = generate_token(user)
    header = {
        'Authorization': 'Bearer {}'.format(token['access_token'])
    }

    response = client.delete(f"{settings.API_V1_STR}/comments/{comment_2.id}", headers=header)
    assert response.status_code == 403

    response = client.delete(f"{settings.API_V1_STR}/comments/{comment_1.id}", headers=header)

    assert response.status_code == 204
