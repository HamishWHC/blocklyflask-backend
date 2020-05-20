from typing import Tuple, Any

from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_optional

from app.models import Project
from app.schemas import DirectorySchema
from app.utils import get_sub_directory_from_path
from app.utils.responses import make_resp, NOT_FOUND

browse_bp = Blueprint("browser", __name__)

directory_schema = DirectorySchema()


@browse_bp.route("/project/<int:project_id>/browse/<path:file_path>/", methods=["GET"])
@browse_bp.route("/project/<string:project_name>/browse/<path:file_path>/", methods=["GET"])
@jwt_optional
def get_dir_contents(project_id: int = None, project_name: str = None, file_path: str = None) -> Tuple[Any, int]:
    project = Project.query.get(project_id) if project_id else Project.query.filter(Project.name == project_name).first()
    if not project:
        return make_resp(NOT_FOUND)
    dir = get_sub_directory_from_path(project.root_directory, file_path)
    return jsonify(data=directory_schema.dump(dir)), 200
