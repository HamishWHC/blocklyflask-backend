from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_optional, get_current_user, create_access_token
import bcrypt
from app.models import User
from webargs.flaskparser import use_args
from webargs.fields import String
from app.schemas import UserSchema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

user_schema = UserSchema(exclude=("projects",))


@auth_bp.route("/login", methods=["POST"], endpoint="login")
@use_args({"username": String(required=True), "password": String(required=True)}, locations=("json",))
def login(args):
    if get_current_user():
        return jsonify(msg="Already authenticated."), 400
    user = User.query.filter_by(username=args.get("username")).first()
    if user and bcrypt.checkpw(args.get("password").encode(), user.hashed_password.encode()):
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token,
                       user=user_schema.dump(user)), 200
    return jsonify(msg="Invalid Credentials"), 401
    