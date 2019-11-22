from typing import Type

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import BaseConfig

db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()
marshmallow = Marshmallow()


def create_app(config: Type[BaseConfig] = BaseConfig) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    marshmallow.init_app(app)
    
    from .blueprints import BLUEPRINTS
    
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
    
    return app
