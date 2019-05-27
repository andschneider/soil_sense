def test_get_sensor_ids(client):
    """Test get the unique sensor ids that have sensor data."""
    response = client.get("/sensor_ids")
    message = response.get_json()
    status = response.status_code

    assert (message["message"], status) == ("success", 200)
