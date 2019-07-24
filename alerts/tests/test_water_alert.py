from unittest.mock import Mock

from main import check_moisture


def test_water_alert():
    data = {"moisture": 500}
    req = Mock(get_json=Mock(return_value=data), args=data)
    req.method = "POST"

    status = check_moisture(req)

    assert status == 200
