class TestUser:
    api_prefix = "/api/v1"
    username = "andrew_new"
    password = "password"

    def test_post_new_user(self, client, token):
        """Test creating a new user"""
        response = client.post(
            self.api_prefix + "/users",
            json={"username": self.username, "password": self.password},
            headers={"Authorization": token},
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 201)

    def test_post_duplicate_user(self, client, token):
        """Test creating a duplicate user"""
        response = client.post(
            self.api_prefix + "/users",
            json={"username": self.username, "password": self.password},
            headers={"Authorization": token},
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"User {self.username} already exists in database.",
            409,
        )

    def test_post_bad_arguments(self, client, token):
        """Test creating a duplicate user. Arguments should be 'username' and 'password'"""
        response = client.post(
            self.api_prefix + "/users",
            json={"user": self.username, "pass": self.password},
            headers={"Authorization": token},
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("Input payload validation failed", 400)

    # @pytest.mark.skip(reason="Would like to check data in db manually")
    def test_delete_new_user(self, client, token):
        """Test deleting a user."""
        response = client.delete(
            self.api_prefix + "/users",
            json={"username": self.username},
            headers={"Authorization": token},
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"User {self.username} successfully deleted",
            200,
        )

    def test_delete_bad_argument(self, client, token):
        """Test deleting a user."""
        response = client.delete(
            self.api_prefix + "/users",
            json={"user": self.username + "_new"},
            headers={"Authorization": token},
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("Input payload validation failed", 400)
