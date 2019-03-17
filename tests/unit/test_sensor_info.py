from unittest.mock import Mock

import pytest
from main import (
    insert_sensor_info,
    get_sensor_info,
    update_sensor_info,
    delete_sensor_info,
)


class TestSensorInfo:
    sensor_id = -1
    plant_name = "Spider"

    def test_post_sensor_info(self):
        data = {"sensor_id": self.sensor_id, "plant": self.plant_name}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = insert_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 201)

    def test_post_sensor_duplicate_info(self):
        data = {"sensor_id": self.sensor_id, "plant": self.plant_name}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = insert_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"sensor id {self.sensor_id} already exists in database. Try updating or deleting first.",
            409,
        )

    def test_post_sensor_info_bad_arguments(self):
        # keys should be 'sensor_id' and 'plant'
        data = {"sensor": self.sensor_id, "plant_name": self.plant_name}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = insert_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 400)

    def test_get_sensor_info(self):
        data = {"sensor_id": self.sensor_id}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = get_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["data"]["sensor_id"], status) == (self.sensor_id, 200)

    def test_get_sensor_info_not_exists(self):
        sensor_id = 99999
        data = {"sensor_id": sensor_id}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = get_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 503)

    def test_get_sensor_info_bad_arguments(self):
        # key should be 'sensor_id'
        data = {"sensor": self.sensor_id}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = get_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 400)

    def test_update_sensor_info(self):
        data = {"sensor_id": self.sensor_id, "plant": "Snake"}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = update_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"Sensor id {self.sensor_id} successfully updated",
            200,
        )

    def test_update_sensor_info_bad_arguments(self):
        # key should be 'sensor_id'
        data = {"sensor": self.sensor_id, "plant": self.plant_name}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = get_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 400)

    # @pytest.mark.skip(reason="Would like to check data in db manually")
    def test_delete_sensor_info(self):
        data = {"sensor_id": self.sensor_id}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = delete_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"Sensor id {self.sensor_id} successfully deleted",
            200,
        )

    def test_delete_sensor_info_bad_arguments(self):
        # key should be 'sensor_id'
        data = {"sensor": self.sensor_id}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # call function and get return data
        response = get_sensor_info(req)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 400)
