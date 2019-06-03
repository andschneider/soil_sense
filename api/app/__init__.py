from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app_settings = getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    # from .endpoints.sensor_data import SensorData
    # from .endpoints.sensor_ids import SensorIds
    from app.api.sensor_info import sensor_info_blueprint

    url_prefix = "/api/v1"
    app.register_blueprint(sensor_info_blueprint, url_prefix=url_prefix)
    # api.add_resource(SensorIds, "/sensor_ids")
    # api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")
    # api.add_resource(SensorData, "/sensor_data")

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
