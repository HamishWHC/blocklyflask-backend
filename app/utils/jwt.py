from flask import jsonify

from app import jwt_manager
from app.models import User
from app.utils.responses import make_resp, UNAUTHORIZED


@jwt_manager.user_loader_callback_loader
def user_loader_callback(identity):
    user = User.query.get(identity)
    if user:
        return user
    else:
        return None


@jwt_manager.user_identity_loader
def user_identity_loader(identity: User):
    return identity.id


@jwt_manager.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return make_resp(UNAUTHORIZED)


@jwt_manager.user_claims_loader
def add_claims_to_access_token(identity: User):
    return {}
