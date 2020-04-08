from typing import Tuple, Any

from flask import jsonify, request, Blueprint

from flask_jwt_extended import jwt_required, get_current_user
from app.models import User
from app.schemas import UserSchema
from app.utils import responses, get_user

users_bp = Blueprint("users", __name__)

user_schema = UserSchema()


@users_bp.route('/users', methods=["GET", "POST"])
@jwt_required
def users() -> Tuple[Any, int]:
    if request.method == "GET":
        return jsonify(data=user_schema.dump(User.query.all(), many=True)), 200
    elif request.method == "POST":
        return responses.NOT_IMPLEMENTED


@users_bp.route("/user", methods=["GET", "PUT", "DELETE"])
@users_bp.route("/user/<int:id>", methods=["GET", "PUT", "DELETE"])
@users_bp.route("/user/<str:username>", methods=["GET", "PUT", "DELETE"])
@jwt_required
def user(id: int, username: str):
    user = get_user(id if id else username if username else None)
    if not user:
        return responses.NOT_FOUND
    if request.method == "GET":
        return jsonify(data=user_schema.dump(user)), 200
    elif request.method == "PUT":
        return responses.NOT_IMPLEMENTED
    elif request.method == "DELETE":
        return responses.NOT_IMPLEMENTED


@users_bp.route("/user", methods=["GET"])
@jwt_required
def user_self():
    if request.method == "GET":
        return jsonify(data=user_schema.dump(get_current_user())), 200
    elif request.method == "PUT":
        return responses.NOT_IMPLEMENTED
    elif request.method == "DELETE":
        return responses.NOT_IMPLEMENTED
