import random
from users.models import User
from argon2 import PasswordHasher
from datetime import datetime, timezone


def generate_token(user: User) -> str:
    salt = "".join([chr(random.randrange(0, 150)) for i in range(256)])
    base_token = user.email + str(user.birthday) + str(user.phone_no) + salt
    token = PasswordHasher().hash(base_token)
    user.x_auth_token = token
    user.x_auth_created_at = datetime.now(timezone.utc)

    user.save()

    return token


def validate_token(user: User, token: str) -> bool:
    if not user.x_auth_token:
        return False

    if user.x_auth_token != token:
        return False

    current_time = datetime.now(timezone.utc)
    token_age = current_time - user.x_auth_created_at
    minutes = token_age.seconds // 60
    hour = minutes // 60

    if hour > 23:
        return False

    if hour == 23 and minutes > 58:
        return False

    return True


def invalidate_token(user: User):
    user.x_auth_token = None
    user.x_auth_created_at = None

    user.save()
