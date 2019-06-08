class TestAuth:
    api_prefix = "/api/v1"

    def test_get_token(self, client):
        data = {"username": "andrew", "password": "password"}
        response = client.post(self.api_prefix + "/auth", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("Successfully logged in.", 200)

    def test_get_token_bad_arguments(self, client):
        data = {"user": "andrew", "pass": "password"}
        response = client.post(self.api_prefix + "/auth", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("Input payload validation failed", 400)

    def test_get_token_doesnt_exist(self, client):
        data = {"username": "dne", "password": "password"}
        response = client.post(self.api_prefix + "/auth", json=data)
        message = response.get_json()
        status = response.status_code

        assert (message["message"], status) == ("User does not exist.", 400)
