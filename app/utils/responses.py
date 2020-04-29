from typing import Tuple
from flask import jsonify


def make_resp(data: Tuple[dict, int]):
    return jsonify(**data[0]), data[1]


NO_JSON = {"msg": "JSON data not present in request."}, 400
NOT_IMPLEMENTED = {"msg": "Not yet implemented."}, 501
NOT_FOUND = {"msg": "That resource does not exist."}, 404
FORBIDDEN = {"msg": "You are forbidden to access this resource."}, 403
UNAUTHORIZED = {"msg": "You must be authenticated to access this resource."}, 401

