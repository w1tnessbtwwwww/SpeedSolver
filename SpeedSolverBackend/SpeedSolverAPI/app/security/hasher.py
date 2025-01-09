import bcrypt


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt(5))

    hashed_password_str = hashed_password.decode('utf-8')

    return hashed_password_str

def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    