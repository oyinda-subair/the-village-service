from typing import List, Any
from app import schemas
from app.models.post import Post
from app.models.user import User


def parse_post_with_user_data(data: Post) -> schemas.post.PostFullResponse:
    return schemas.post.PostFullResponse(
        id=data.id,
        title=data.title,
        description=data.description,
        content=data.content,
        category=data.category,
        image_url=data.image_url,
        user_id=data.user_id,
        created_at=data.created_at,
        updated_at=data.updated_at,
        user=schemas.post.PostFilteredUserResponse(first_name=data.user.first_name, surname=data.user.surname)
    )


def parse_post_with_user_data_list(posts: List[Post]) -> List[schemas.post.PostFullResponse]:
    return list(map(parse_post_with_user_data, posts))


def parse_complete_user_data(data: User) -> schemas.User:
    return schemas.User(
        id=data.id,
        first_name=data.first_name,
        surname=data.surname,
        email=data.email,
        is_superuser=data.is_superuser,
        role=data.role,
        # posts=data.posts,
        # comments=data.comments
    )


def parse_complete_user_data_list(users: Any) -> List[schemas.User]:
    return list(map(parse_complete_user_data, users))
