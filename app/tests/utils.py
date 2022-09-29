from app.core.authentication import create_access_token
import random
import string


def generate_token(user):
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


def get_random_string():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(8))
