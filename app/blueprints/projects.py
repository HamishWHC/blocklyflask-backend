from typing import Tuple, Any

from flask import jsonify, request, Blueprint

from flask_jwt_extended import jwt_required, get_current_user
from app.models import Project
from app.schemas import ProjectSchema
from app.utils import responses, get_user

projects_bp = Blueprint("users", __name__)

project_schema = ProjectSchema()


@projects_bp.route('/projects', methods=["GET", "POST"])
@projects_bp.route('/user/<int:user_id>/projects', methods=["GET", "POST"])
@projects_bp.route('/user/<str:username>/projects', methods=["GET", "POST"])
@jwt_required
def block_files(user_id: int, username: str) -> Tuple[Any, int]:
    user = get_user(user_id if user_id else username if username else None)
    if not user:
        return responses.NOT_FOUND
    if request.method == "GET":
        return jsonify(data=project_schema.dump(Project.query.filter(Project.user_id == user.id).all(),
                                                   many=True)), 200
    elif request.method == "POST":
        return responses.NOT_IMPLEMENTED


@projects_bp.route("/project/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required
def project(id: int):
    project = Project.query.get(id)
    if not project:
        return responses.NOT_FOUND
    if request.method == "GET":
        return jsonify(data=project_schema.dump(project)), 200
    elif request.method == "PUT":
        return responses.NOT_IMPLEMENTED
    elif request.method == "DELETE":
        return responses.NOT_IMPLEMENTED
