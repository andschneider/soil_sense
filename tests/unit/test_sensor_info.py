from unittest.mock import Mock

from main import get_sensor_info


def test_get_sensor_info():
    sensor_id = 1
    data = {"sensor_id": sensor_id}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # call function and get return data
    response = get_sensor_info(req)
    message = response.get_json()
    status = response.status_code

    assert (message["data"]["sensor_id"], status) == (sensor_id, 200)


def test_get_sensor_info_bad_input():
    sensor_id = 99999
    data = {"sensor_id": sensor_id}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # call function and get return data
    response = get_sensor_info(req)
    message = response.get_json()
    status = response.status_code

    assert (message["message"], status) == ("fail", 503)
