from typing import Tuple, Any

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_optional, create_access_token
from marshmallow import ValidationError
from webargs.fields import String, Integer
from webargs.flaskparser import use_args

from app import db
from app.models import User
from app.schemas import UserSchema
from app.utils import get_user
from app.utils.responses import make_resp, NOT_FOUND, NO_JSON, FORBIDDEN

users_bp = Blueprint("users", __name__)

user_schema = UserSchema()
other_user_schema = UserSchema(exclude=("email",))


@users_bp.route('/users/', methods=["POST"])
@jwt_optional
def users_post() -> Tuple[Any, int]:
    if get_user() is not None:
        return make_resp(FORBIDDEN)
    if not request.is_json:
        return make_resp(NO_JSON)
    try:
        user = user_schema.load(request.get_json())
    except ValidationError as errors:
        return errors.messages, 422
    db.session.add(user)
    db.session.commit()
    return jsonify(data=user_schema.dump(user), access_token=create_access_token(identity=user)), 200


@users_bp.route("/user/", methods=["GET", "PUT", "DELETE"])
@users_bp.route("/user/<int:id>/", methods=["GET"])
@users_bp.route("/user/<string:username>/", methods=["GET"])
@jwt_optional
def user(id: int = None, username: str = None) -> Tuple[Any, int]:
    user = get_user(id if id else username.lower() if username else None)
    if not user:
        return make_resp(NOT_FOUND)
    if request.method == "GET":
        return jsonify(data=user_schema.dump(user) if get_user() == user else other_user_schema.dump(user)), 200
    elif request.method == "PUT":
        if user != get_user():
            return make_resp(FORBIDDEN)
        if not request.is_json:
            return make_resp(NO_JSON)
        try:
            user_schema.context["user_id"] = user.id
            user = user_schema.load(request.get_json(), instance=user)
            user_schema.context.pop("user_id")
        except ValidationError as errors:
            return errors.messages, 422
        db.session.commit()
        return jsonify(data=user_schema.dump(user)), 200
    elif request.method == "DELETE":
        if user != get_user():
            return make_resp(FORBIDDEN)
        db.session.delete(user)
        db.session.commit()
        return make_resp(({"msg": "success"}, 200))


@users_bp.route("/uniquity-check/username/", methods=["GET"])
@use_args({"username": String(required=True), "user_id": Integer(required=False)}, locations=("querystring",))
def username_check(args) -> Tuple[Any, int]:
    return jsonify(
        taken=User.query.filter(
            User.username == args.get("username", "").lower(),
            User.id != args.get("user_id", 0)
        ).first() is not None), 200


@users_bp.route("/uniquity-check/email/", methods=["GET"])
@use_args({"email": String(required=True), "user_id": Integer(required=False)}, locations=("querystring",))
def email_check(args) -> Tuple[Any, int]:
    return jsonify(
        taken=User.query.filter(
            User.email == args.get("email", "").lower(),
            User.id != args.get("user_id", 0)
        ).first() is not None
    ), 200
