from typing import Tuple, Any

import bcrypt
from flask import Blueprint, jsonify
from flask_jwt_extended import get_current_user, create_access_token
from webargs.fields import String
from webargs.flaskparser import use_args

from app.models import User
from app.schemas import UserSchema

auth_bp = Blueprint("auth", __name__)

user_schema = UserSchema(exclude=("projects",))


@auth_bp.route("/auth/", methods=["POST"])
@use_args({"email": String(required=True), "password": String(required=True)}, locations=("json",))
def login(args) -> Tuple[Any, int]:
    """
    Authenticates a user using an email and password, returning an appropriate response.
    :param args: Dictionary object from webargs (a library that makes request arguments easier to use)
        containing the provided email and password.
    :return: Either a JSON error response (400 or 401), or a valid access token,
        plus the data of the authenticated user (200 OK).
    """

    # If user is already authenticated, get_current_user() will return a truthy value
    # and immediately return a JSON response.
    if get_current_user():
        # Provides helpful error to API user, along with a 400 (Bad Request)
        # status code indicating a mistake on the user's part.
        return jsonify(msg="Already authenticated (you already have a token!)."), 400

    # This searches the user table for a user with the email provided
    # (made lowercase to prevent case-sensitivity on the email).
    # Emails are unique so simply getting the first one is fine. If there is no user with the given email, .first()
    # will return None (Python equivalent of null).
    user = User.query.filter_by(email=args.get("email", "").lower()).first()

    # If the user exists AND the hash of the given password matches the stored hashed password of the user...
    if user and bcrypt.checkpw(args.get("password").encode(), user.hashed_password.encode()):
        # Create a new access token using the user as the identity.
        access_token = create_access_token(identity=user)
        # Return a JSON object containing the new access token, in addition to the user's data
        # (limited by UserSchema, i.e. password is not provided, see schemas/user.py).
        return jsonify(access_token=access_token,
                       user=user_schema.dump(user)), 200
    return jsonify(msg="Invalid credentials."), 401
