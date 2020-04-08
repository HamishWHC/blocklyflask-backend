from typing import Tuple, Any

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import BlockFile
from app.schemas import BlockFileSchema
from app.utils import responses

block_files_bp = Blueprint("users", __name__)

block_file_schema = BlockFileSchema()


@block_files_bp.route('/project/<int:project_id>/block-files', methods=["GET", "POST"])
@jwt_required
def block_files(project_id: int) -> Tuple[Any, int]:
    if request.method == "GET":
        return jsonify(data=block_file_schema.dump(BlockFile.query.filter(BlockFile.project_id == project_id).all(),
                                                   many=True)), 200
    elif request.method == "POST":
        return responses.NOT_IMPLEMENTED


@block_files_bp.route("/block-file/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required
def block_file(id: int):
    block_file = BlockFile.query.get(id)
    if not block_file:
        return responses.NOT_FOUND
    if request.method == "GET":
        return jsonify(data=block_file_schema.dump(block_file)), 200
    elif request.method == "PUT":
        return responses.NOT_IMPLEMENTED
    elif request.method == "DELETE":
        return responses.NOT_IMPLEMENTED
