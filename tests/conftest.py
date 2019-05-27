import pytest
from flask import Flask
from flask_restful import Api

from endpoints.sensor_data import SensorData
from endpoints.sensor_ids import SensorIds
from endpoints.sensor_info import SensorInfo


@pytest.fixture(scope="module")
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True

    api = Api(app)

    api.add_resource(SensorIds, "/sensor_ids")
    api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")
    api.add_resource(SensorData, "/sensor_data")

    client = app.test_client()

    yield client
