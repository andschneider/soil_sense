from unittest.mock import Mock

import pytest

from main import check_moisture


def test_water_alert():
    data = {"moisture": 500}
    req = Mock(get_json=Mock(return_value=data), args=data)
    req.method = "POST"

    response = check_moisture(req)

    message = response.get_json()
    status = response.status_code

    assert (message["message"], status) == ("alert completed successfully", 200)


def test_water_alert_bad_data():
    data = {"moisture": None}
    req = Mock(get_json=Mock(return_value=data), args=data)
    req.method = "POST"

    response = check_moisture(req)

    message = response.get_json()
    status = response.status_code

    assert (message["message"], status) == ("moisture value must be supplied", 400)


@pytest.mark.xfail
def test_water_alert_string_data():
    data = {"moisture": "fail"}
    req = Mock(get_json=Mock(return_value=data), args=data)
    req.method = "POST"

    response = check_moisture(req)

    message = response.get_json()
    status = response.status_code

    assert (message["message"], status) == ("moisture value must be supplied", 400)
