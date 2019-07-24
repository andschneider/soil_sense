import os

import requests


class SensorAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:3030")
        self.api_prefix = "/api/v1"
        self._token = self._authenticate()

    def _authenticate(self):
        username = os.getenv("API_USERNAME")
        password = os.getenv("API_PASSWORD")
        url = self.base_url + self.api_prefix + "/auth"

        response = requests.post(url, json={"username": username, "password": password})

        if response.status_code != 200:
            raise ConnectionRefusedError("Could not authenticate with API.")

        return "Bearer " + response.json()["auth_token"]

    def get_sensor_ids(self):
        url = self.base_url + self.api_prefix + "/sensor_ids"
        r = requests.get(url, headers={"Authorization": self._token})
        return r.status_code, r.json()

    def get_sensor_data(self, minutes, sensor_ids):
        url = self.base_url + self.api_prefix + "/sensor_data"

        id_string = ",".join([str(s_id) for s_id in sensor_ids])
        args = f"sensor_ids={id_string}&minutes={minutes}"

        full_url = url + "?" + args
        r = requests.get(full_url, headers={"Authorization": self._token})

        if r.status_code == 200:
            return r.json()
        # TODO catch api errors
        # return r.status_code, r.json()

    def get_plant_by_id(self, sensor_id):
        url = self.base_url + self.api_prefix + "/sensor_info/" + str(sensor_id)
        r = requests.get(url, headers={"Authorization": self._token})

        return r.status_code, r.json()
