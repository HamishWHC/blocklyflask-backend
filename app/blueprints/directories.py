import datetime
from typing import Tuple, Any

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_optional
from marshmallow import ValidationError

from app import db
from app.models import Directory, Project
from app.schemas import DirectorySchema
from app.utils.helpers import get_user, get_sub_directory_from_path
from app.utils.responses import make_resp, NOT_FOUND, UNAUTHORIZED, FORBIDDEN, NO_JSON

directory_bp = Blueprint("directories", __name__)

directory_schema = DirectorySchema()
in_directory_schema = DirectorySchema(exclude=("parent_id",))

# @directory_bp.route('/project/<int:project_id>/directories/', methods=["POST"])
# @directory_bp.route('/project/<string:project_name>/directories/', methods=["POST"])
# @jwt_optional
# def create_project_directory(project_id: int = None, project_name: str = None) -> Tuple[Any, int]:
#     project = Project.query.get(project_id) if project_id else Project.query.filter(Project.name == project_name).first()
#     if not project:
#         return make_resp(NOT_FOUND)
#     if not get_user():
#         return make_resp(UNAUTHORIZED)
#     if project.user != get_user():
#         return make_resp(FORBIDDEN)
#     if not request.is_json:
#         return make_resp(NO_JSON)
#     try:
#         directory = directory_schema.load(request.get_json())
#         project.last_modified = datetime.datetime.now()
#     except ValidationError as errors:
#         return errors.messages, 422
#     db.session.add(directory)
#     db.session.commit()
#     return jsonify(data=directory_schema.dump(directory)), 200

@directory_bp.route("/project/<int:project_id>/create-directory-in/", methods=["POST"])
@directory_bp.route("/project/<string:project_name>/create-directory-in/", methods=["POST"])
@directory_bp.route("/project/<int:project_id>/create-directory-in/<path:parent_dir_path>/", methods=["POST"])
@directory_bp.route("/project/<string:project_name>/create-directory-in/<path:parent_dir_path>/", methods=["POST"])
@jwt_optional
def create_directory_with_path(project_id: int = None, project_name: str = None, parent_dir_path: str = "") -> Tuple[Any, int]:
    project = Project.query.get(project_id) if project_id else Project.query.filter(
        Project.name == project_name.lower()).first()
    if not get_user():
        return make_resp(UNAUTHORIZED)
    if not project:
        return make_resp(NOT_FOUND)
    if project.user != get_user():
        return make_resp(FORBIDDEN)
    if not request.is_json:
        return make_resp(NO_JSON)
    parent_dir = get_sub_directory_from_path(project.root_directory, parent_dir_path)
    if not parent_dir:
        return make_resp(NOT_FOUND)
    try:
        directory = in_directory_schema.load(request.get_json())
        directory.parent = parent_dir
        project.last_modified = datetime.datetime.now()
    except ValidationError as errors:
        return errors.messages, 422
    db.session.add(directory)
    db.session.commit()
    return jsonify(data=directory_schema.dump(directory)), 200


@directory_bp.route("/directory/<int:id>/", methods=["GET", "PUT", "DELETE"])
@jwt_optional
def directory(id: int) -> Tuple[Any, int]:
    directory = Directory.query.get(id)
    if not directory:
        return make_resp(NOT_FOUND)
    if request.method == "GET":
        return jsonify(data=directory_schema.dump(directory)), 200
    elif request.method == "PUT":
        if directory.project.user != get_user():
            return make_resp(FORBIDDEN)
        if not request.is_json:
            return make_resp(NO_JSON)
        try:
            directory = directory_schema.load(request.get_json(), instance=directory, partial=True)
            directory.project.last_modified = datetime.datetime.now()
        except ValidationError as errors:
            return errors.messages, 422
        db.session.commit()
        return jsonify(data=directory_schema.dump(directory)), 200
    elif request.method == "DELETE":
        if directory.project.user != get_user():
            return make_resp(FORBIDDEN)
        db.session.delete(directory)
        db.session.commit()
        return make_resp(({"msg": "success"}, 200))
