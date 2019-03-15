import json
from unittest.mock import Mock

from main import get_sensor_info


def test_get_sensor_info():
    sensor_id = 1
    data = {"sensor_id": sensor_id}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # call function and get return data
    response, status, _ = get_sensor_info(req)
    response = json.loads(response)

    assert (response["data"]["sensor_id"], status) == (sensor_id, 200)
