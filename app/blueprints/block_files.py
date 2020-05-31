import datetime
from typing import Tuple, Any

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_optional
from marshmallow import ValidationError

from app import db
from app.models import BlockFile, Project
from app.schemas import BlockFileSchema
from app.utils.helpers import get_user, get_sub_directory_from_path
from app.utils.responses import make_resp, NOT_FOUND, UNAUTHORIZED, FORBIDDEN, NO_JSON

block_files_bp = Blueprint("block_files", __name__)

block_file_schema = BlockFileSchema()
in_block_file_schema = BlockFileSchema(exclude=("directory_id",))


# @block_files_bp.route('/project/<int:project_id>/block-files/', methods=["GET", "POST"])
# @block_files_bp.route('/project/<string:project_name>/block-files/', methods=["GET", "POST"])
# @jwt_optional
# def get_project_block_files(project_id: int = None, project_name: str = None) -> Tuple[Any, int]:
#     project = Project.query.get(project_id) if project_id else Project.query.filter(Project.name == project_name).first()
#     if not project:
#         return make_resp(NOT_FOUND)
#     if request.method == "GET":
#         return jsonify(data=block_file_schema.dump(project.block_files, many=True)), 200
#     elif request.method == "POST":
#         if not get_user():
#             return make_resp(UNAUTHORIZED)
#         if project.user != get_user():
#             return make_resp(FORBIDDEN)
#         if not request.is_json:
#             return make_resp(NO_JSON)
#         try:
#             block_file = block_file_schema.load(request.get_json())
#             block_file.project.last_modified = datetime.datetime.utcnow()
#         except ValidationError as errors:
#             return errors.messages, 422
#         db.session.add(block_file)
#         db.session.commit()
#         return jsonify(data=block_file_schema.dump(block_file)), 200


@block_files_bp.route("/project/<int:project_id>/create-file-in/", methods=["POST"])
@block_files_bp.route("/project/<string:project_name>/create-file-in/", methods=["POST"])
@block_files_bp.route("/project/<int:project_id>/create-file-in/<path:file_path>/", methods=["POST"])
@block_files_bp.route("/project/<string:project_name>/create-file-in/<path:file_path>/", methods=["POST"])
@jwt_optional
def create_block_file(project_id: int = None, project_name: str = None, file_path: str = "") -> Tuple[Any, int]:
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
    dir = get_sub_directory_from_path(project.root_directory, file_path)
    if not dir:
        return make_resp(NOT_FOUND)
    try:
        block_file = in_block_file_schema.load(request.get_json())
        block_file.directory = dir
        project.last_modified = datetime.datetime.utcnow()
    except ValidationError as errors:
        return errors.messages, 422
    db.session.add(block_file)
    db.session.commit()
    return jsonify(data=block_file_schema.dump(block_file)), 200


@block_files_bp.route("/block-file/<int:id>/", methods=["GET", "PUT", "DELETE"])
@jwt_optional
def block_file(id: int) -> Tuple[Any, int]:
    block_file = BlockFile.query.get(id)
    if not block_file:
        return make_resp(NOT_FOUND)
    if request.method == "GET":
        return jsonify(data=block_file_schema.dump(block_file)), 200
    elif request.method == "PUT":
        if block_file.project.user != get_user():
            return make_resp(FORBIDDEN)
        if not request.is_json:
            return make_resp(NO_JSON)
        try:
            block_file = block_file_schema.load(request.get_json(), instance=block_file, partial=True)
            block_file.project.last_modified = datetime.datetime.utcnow()
        except ValidationError as errors:
            return errors.messages, 422
        db.session.commit()
        return jsonify(data=block_file_schema.dump(block_file)), 200
    elif request.method == "DELETE":
        if block_file.project.user != get_user():
            return make_resp(FORBIDDEN)
        db.session.delete(block_file)
        db.session.commit()
        return make_resp(({"msg": "success"}, 200))
