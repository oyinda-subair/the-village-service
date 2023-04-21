import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), bytes(hashed_password, 'utf-8'))


def get_password_hash(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return hashed_password.decode('utf8')
