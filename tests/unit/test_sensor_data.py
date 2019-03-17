from unittest.mock import Mock

import pytest
from main import insert_data, get_sensor_data


class TestSensorData:
    sensor_id = -10
    temperature = -9
    moisture = -8

    def test_post_sensor_data(self):
        data = {
            "sensor_id": self.sensor_id,
            "temperature": self.temperature,
            "moisture": self.moisture,
        }
        req = Mock(get_json=Mock(return_value=data), args=data)

        response = insert_data(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 201)

    def test_post_sensor_data_bad_arguments(self):
        # keys should be 'sensor_id' and 'temperature'
        data = {
            "sensor": self.sensor_id,
            "temp": self.temperature,
            "moisture": self.moisture,
        }
        req = Mock(get_json=Mock(return_value=data), args=data)

        response = insert_data(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 400)

    def test_get_sensor_data(self):
        data = {"sensor_ids": "1, -10", "minutes": 10}
        req = Mock(get_json=Mock(return_value=data), args=data)

        response = get_sensor_data(req)
        message = response.get_json()
        status = response.status_code
        # print(message["data"].keys())

        assert status == 200

    def test_get_sensor_data_bad_arguments(self):
        # keys should be 'sensor_ids' and 'minutes'
        data = {"sensor_id": "1,2", "minut": 10}
        req = Mock(get_json=Mock(return_value=data), args=data)

        response = get_sensor_data(req)
        message = response.get_json()
        status = response.status_code

        assert status == 200
