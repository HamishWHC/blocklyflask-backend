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
    
    return app
