import json


class TestUser:
    api_prefix = "/api/v1"
    username = "andrew"
    password = "password"

    def test_post_new_user(self, client):
        """Test creating a new user"""
        response = client.post(
            self.api_prefix + "/users",
            json={
                "username": self.username + "_new",
                "password": self.password + "_new",
            },
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("success", 201)

    def test_post_duplicate_user(self, client):
        """Test creating a duplicate user"""
        response = client.post(
            self.api_prefix + "/users",
            json={"username": self.username, "password": self.password},
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == (
            f"User {self.username} already exists in database.",
            409,
        )

    def test_post_bad_arguments(self, client):
        """Test creating a duplicate user. Arguments should be 'username' and 'password'"""
        response = client.post(
            self.api_prefix + "/users",
            json={"user": self.username, "pass": self.password},
        )
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("Input payload validation failed", 400)
