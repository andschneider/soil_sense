from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app_settings = getenv("APP_SETTINGS", "default")
    app.config.from_object(config[app_settings])

    db.init_app(app)

    from api.endpoints.sensor_info import sensor_info_blueprint
    from api.endpoints.sensor_ids import sensor_ids_blueprint

    url_prefix = "/api/v1"
    app.register_blueprint(sensor_info_blueprint, url_prefix=url_prefix)
    app.register_blueprint(sensor_ids_blueprint, url_prefix=url_prefix)
    # api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")
    # api.add_resource(SensorData, "/sensor_data")

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
