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
@use_args({"username": String(required=True), "password": String(required=True)}, locations=("json",))
def login(args):
    if get_current_user():
        return jsonify(msg="Already authenticated (you already have a token!)."), 400
    user = User.query.filter_by(username=args.get("username")).first()
    if user and bcrypt.checkpw(args.get("password").encode(), user.hashed_password.encode()):
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token,
                       user=user_schema.dump(user)), 200
    return jsonify(msg="Invalid credentials."), 401
