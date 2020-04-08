from typing import Union
from app.models import User
from flask_jwt_extended import get_current_user


def get_user(identifier: Union[int, str, None]) -> Union[User, None]:
    if isinstance(identifier, int):
        return User.query.get(identifier)
    elif isinstance(identifier, str):
        return User.query.filter(User.username == identifier).first()
    elif identifier is None:
        return get_current_user()
    else:
        return None