from unittest.mock import Mock

import pytest
from flask import Flask
from flask_restful import Api

from endpoints.sensor_info import SensorInfo


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True

    api = Api(app)
    api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")

    client = app.test_client()

    yield client


def test_get_sensor_info(client):
    response = client.get("/sensor_info/1")
    message = response.get_json()
    status = response.status_code

    assert (message["message"], status) == ("success", 200)
