def test_get_sensor_ids(client, token):
    """Test get the unique sensor ids that have sensor data."""
    response = client.get("/api/v1/sensor_ids", headers={"Authorization": token})
    message = response.get_json()
    status = response.status_code

    assert (message["message"], status) == ("success", 200)
