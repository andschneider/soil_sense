class TestSensorData:
    sensor_id = 999
    temperature = -9
    moisture = -8

    def test_post_sensor_data(self, client):
        """Test create sensor data."""
        data = {
            "sensor_id": self.sensor_id,
            "temperature": self.temperature,
            "moisture": self.moisture,
        }
        response = client.post("/sensor_data", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 201)

    def test_post_sensor_data_bad_arguments(self, client):
        """Test passing in bad data. Keys should be 'sensor_id' and 'temperature'."""
        data = {
            "sensor": self.sensor_id,
            "temp": self.temperature,
            "moisture": self.moisture,
        }
        response = client.post("/sensor_data", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            "['sensor_id', 'temperature'] were not supplied.",
            400,
        )

    def test_get_sensor_data_single(self, client):
        """Test getting data back for a single sensor id."""
        data = {"sensor_ids": f"{self.sensor_id}", "minutes": 10}

        response = client.get("/sensor_data", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 200)

    def test_get_sensor_data_multiple(self, client):
        """Test getting data back for multiple sensor ids."""
        data = {"sensor_ids": f"1, {self.sensor_id}", "minutes": 10}

        response = client.get("/sensor_data", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 200)

    def test_get_sensor_data_bad_arguments(self, client):
        """Test passing in bad arguments. Keys should be 'sensor_ids' and 'minutes'."""
        data = {"sensor_id": "1", "minut": 10}

        response = client.get("/sensor_data", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 503)
