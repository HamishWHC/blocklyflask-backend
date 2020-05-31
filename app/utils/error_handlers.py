from typing import Tuple, Any

from flask import jsonify


def handle_404(*args) -> Tuple[Any, int]:
    return jsonify({"msg": "The requested resource could not be found."}), 404


def handle_403(*args) -> Tuple[Any, int]:
    return jsonify({"msg": "You are forbidden from accessing this resource."}), 403


def handle_401(*args) -> Tuple[Any, int]:
    return jsonify({"msg": "You are not authorized to access this resource."}), 401


def handle_400(*args) -> Tuple[Any, int]:
    return jsonify({"msg": "The request was invalid."}), 400


def handle_500(*args) -> Tuple[Any, int]:
    return jsonify({
        "msg": "An internal server error occurred! Please raise an issue at https://github.com/HamishWHC/blocklyflask-backend/"
    }), 500
