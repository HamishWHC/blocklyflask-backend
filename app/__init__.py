from typing import Type

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .config import BaseConfig

db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()
marshmallow = Marshmallow()
cors = CORS()


def create_app(config: Type[BaseConfig] = BaseConfig) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    marshmallow.init_app(app)
    cors.init_app(app)

    import app.models as MODELS
    import app.utils as UTILS
    import app.schemas as SCHEMAS

    from .blueprints import BLUEPRINTS

    for bp in BLUEPRINTS:
        app.register_blueprint(bp)

    app.register_error_handler(404, UTILS.handle_404)
    app.register_error_handler(403, UTILS.handle_403)
    app.register_error_handler(401, UTILS.handle_401)
    app.register_error_handler(400, UTILS.handle_400)
    app.register_error_handler(500, UTILS.handle_500)
    app.register_error_handler(405, UTILS.handle_405)

    return app
