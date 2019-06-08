from os import getenv

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app_settings = getenv("APP_SETTINGS", "default")
    app.config.from_object(config[app_settings])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from api.endpoints.sensor_info import sensor_info_blueprint
    from api.endpoints.sensor_ids import sensor_ids_blueprint
    from api.endpoints.sensor_data import sensor_data_blueprint
    from api.endpoints.user import users_blueprint
    from api.endpoints.auth import auth_blueprint

    url_prefix = "/api/v1"
    app.register_blueprint(sensor_info_blueprint, url_prefix=url_prefix)
    app.register_blueprint(sensor_ids_blueprint, url_prefix=url_prefix)
    app.register_blueprint(sensor_data_blueprint, url_prefix=url_prefix)
    app.register_blueprint(users_blueprint, url_prefix=url_prefix)
    app.register_blueprint(auth_blueprint, url_prefix=url_prefix)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
