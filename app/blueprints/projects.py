import datetime
from typing import Tuple, Any

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_optional
from marshmallow import ValidationError

from app import db
from app.models import Project, Directory
from app.schemas import ProjectSchema
from app.utils import get_user
from app.utils.responses import make_resp, NOT_FOUND, NO_JSON, FORBIDDEN, UNAUTHORIZED

projects_bp = Blueprint("projects", __name__)

project_schema = ProjectSchema()


@projects_bp.route('/projects/', methods=["GET", "POST"])
@projects_bp.route('/user/<int:user_id>/projects/', methods=["GET"])
@projects_bp.route('/user/<string:username>/projects/', methods=["GET"])
@jwt_optional
def projects(user_id: int = None, username: str = None) -> Tuple[Any, int]:
    user = get_user(user_id if user_id else username if username else None)
    if not user:
        return make_resp(NOT_FOUND)
    if request.method == "GET":
        return jsonify(data=project_schema.dump(Project.query.filter(Project.user_id == user.id).all(),
                                                many=True)), 200
    elif request.method == "POST":
        if get_user() is None:
            return make_resp(UNAUTHORIZED)
        if not request.is_json:
            return make_resp(NO_JSON)
        try:
            project = project_schema.load(request.get_json())
            project.user = get_user()
            project.root_directory = Directory(name="root")
            project.last_modified = datetime.datetime.now()
        except ValidationError as errors:
            return errors.messages, 422
        db.session.add(project)
        db.session.commit()
        return jsonify(data=project_schema.dump(project)), 200


@projects_bp.route("/project/<int:id>/", methods=["GET", "PUT", "DELETE"])
@projects_bp.route("/project/<string:name>/", methods=["GET", "PUT", "DELETE"])
@jwt_optional
def project(id: int = None, name: str = None) -> Tuple[Any, int]:
    project = Project.query.get(id) if id else Project.query.filter(Project.name == name).first()
    if not project:
        return make_resp(NOT_FOUND)
    if request.method == "GET":
        return jsonify(data=project_schema.dump(project)), 200
    elif request.method == "PUT":
        if project.user != get_user():
            return make_resp(FORBIDDEN)
        if not request.is_json:
            return make_resp(NO_JSON)
        try:
            project = project_schema.load(request.get_json(), instance=project)
            project.last_modified = datetime.datetime.now()
        except ValidationError as errors:
            return errors.messages, 422
        db.session.commit()
        return jsonify(data=project_schema.dump(project)), 200
    elif request.method == "DELETE":
        if project.user != get_user():
            return make_resp(FORBIDDEN)
        db.session.delete(project)
        db.session.commit()
        return make_resp(({"msg": "success"}, 200))
