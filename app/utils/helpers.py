from typing import Union, Callable
from app.models import User
from flask_jwt_extended import get_current_user
from marshmallow import ValidationError


def get_user(identifier: Union[int, str, None] = None) -> Union[User, None]:
    if isinstance(identifier, int):
        return User.query.get(identifier)
    elif isinstance(identifier, str):
        return User.query.filter(User.username == identifier).first()
    elif identifier is None:
        return get_current_user()
    else:
        return None


def exists(table, name: str) -> Callable:
    def _exists(value: int) -> None:
        if not table.query.get(value):
            raise ValidationError("There is no " + name + " with ID " + str(value) + ".")

    return _exists
