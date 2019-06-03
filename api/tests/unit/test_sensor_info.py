class TestSensorInfo:
    sensor_id = 999
    plant_name = "Spider"

    def test_post_sensor_info(self, client):
        """Test creating a new sensor id entry."""
        response = client.post(
            f"/sensor_info/{self.sensor_id}", json={"plant": self.plant_name}
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 201)

    def test_post_sensor_duplicate_info(self, client):
        """Test creating a duplicate sensor id entry."""
        response = client.post(
            f"/sensor_info/{self.sensor_id}", json={"plant": self.plant_name}
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"Sensor id {self.sensor_id} already exists in database. Try updating or deleting first.",
            409,
        )

    def test_post_sensor_info_bad_arguments(self, client):
        """Test passing in bad data. Key should be 'plant' not 'plant_name'."""
        response = client.post(
            f"/sensor_info/{self.sensor_id}", json={"plant_name": self.plant_name}
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 503)

    def test_get_sensor_info(self, client):
        """Test getting sensor information for a given sensor id."""
        response = client.get(f"/sensor_info/{self.sensor_id}")
        response = client.get(f"/sensor_info/1")
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 200)

    def test_get_sensor_info_not_exists(self, client):
        """Test getting sensor information that isn't in the database."""
        sensor_id = 99999
        response = client.get(f"/sensor_info/{sensor_id}")
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 503)

    def test_update_sensor_info(self, client):
        """Test updating the plant name for a given sensor id."""
        new_name = "Snake"
        response = client.put(
            f"/sensor_info/{self.sensor_id}", json={"plant": new_name}
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"Sensor id {self.sensor_id} successfully updated",
            200,
        )

    def test_update_sensor_info_bad_arguments(self, client):
        """Test passing in bad data. Key should be 'plant' not 'plant_name'."""
        response = client.put(
            f"/sensor_info/{self.sensor_id}", json={"plant_name": self.plant_name}
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("fail", 503)

    # @pytest.mark.skip(reason="Would like to check data in db manually")
    def test_delete_sensor_info(self, client):
        """Test deleting the row for a given sensor id."""
        response = client.delete(f"/sensor_info/{self.sensor_id}")
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"Sensor id {self.sensor_id} successfully deleted",
            200,
        )
