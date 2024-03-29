import os
import factory
from faker import Factory as FakerFactory
from app.models.comment import Comment

from app.models.user import User
from app.models.post import Post
from app.core.security import get_password_hash
from app.schemas.base import UserRole
from app.tests.utils.base_factory import BaseFactory
from app.tests.utils.helper import get_random_word

faker = FakerFactory.create()


class UserFactory(BaseFactory):
    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda x: faker.name().split(' ')[0])
    surname = factory.LazyAttribute(lambda x: faker.name().split(' ')[1])
    email = factory.Sequence(lambda a: 'person_{}@example.com'.format(get_random_word()).lower())
    is_superuser = False
    hashed_password = get_password_hash(faker.password())
    role = UserRole.USER


class PostFactory(BaseFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    description = factory.Faker('paragraph')
    content = factory.Faker('paragraph')
    category = factory.Faker("sentence", nb_words=1, variable_nb_words=True)
    image_url = factory.Sequence(lambda a: 'http://image_url_{}@example.com'.format(a).lower())
    user = factory.SubFactory(UserFactory)


class CommentFactory(BaseFactory):
    class Meta:
        model = Comment

    content = factory.Faker("sentence", nb_words=10, variable_nb_words=True)
    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
