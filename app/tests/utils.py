from app.core.authentication import create_access_token


def generate_token(user):
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }
