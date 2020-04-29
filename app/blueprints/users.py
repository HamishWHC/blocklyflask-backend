from typing import Tuple, Any

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_optional, get_current_user

from marshmallow import ValidationError
from app import db
from app.models import User
from app.schemas import UserSchema
from app.utils import get_user
from app.utils.responses import make_resp, NOT_IMPLEMENTED, NOT_FOUND, NO_JSON, FORBIDDEN

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
    return jsonify(data=user_schema.dump(user)), 200


@users_bp.route("/user/", methods=["GET", "PUT", "DELETE"])
@users_bp.route("/user/<int:id>/", methods=["GET"])
@users_bp.route("/user/<string:username>/", methods=["GET"])
@jwt_optional
def user(id: int = None, username: str = None):
    user = get_user(id if id else username if username else None)
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
            user = user_schema.load(request.get_json(), instance=user)
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
