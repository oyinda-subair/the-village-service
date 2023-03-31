import os
from app.core.authentication import create_access_token
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def generate_token(user):
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


def get_random_string():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(8))


def get_random_word():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(8))


def get_random_sentence():
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs")
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")

    l = [nouns, verbs, adj, adv]
    return ''.join([random.choice(i) for i in l])


# TEST_SQLALCHEMY_DATABASE_URL = os.environ.get("TEST_DATABASE_URI")

# engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
