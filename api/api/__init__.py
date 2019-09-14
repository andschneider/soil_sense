from os import getenv

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from .config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app_settings = getenv("APP_SETTINGS", "default")
    app.config.from_object(config[app_settings])

    doc_prefix = "/api/docs"
    api = Api(
        title="soil sense",
        version="1.0.0",
        description="soil sense api",
        doc=doc_prefix,
        security="Bearer Auth",
        authorizations={
            "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"}
        },
    )

    from api.endpoints.auth import api as auth
    from api.endpoints.user import api as users
    from api.endpoints.health import api as health
    from api.endpoints.sensor_ids import api as sensor_ids
    from api.endpoints.sensor_info import api as sensor_info
    from api.endpoints.sensor_data import api as sensor_data

    url_prefix = "/api/v1"
    api.add_namespace(auth, path=url_prefix)
    api.add_namespace(users, path=url_prefix)
    api.add_namespace(health, path=url_prefix)
    api.add_namespace(sensor_ids, path=url_prefix)
    api.add_namespace(sensor_info, path=url_prefix)
    api.add_namespace(sensor_data, path=url_prefix)

    api.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt._set_error_handler_callbacks(api)
    jwt.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
