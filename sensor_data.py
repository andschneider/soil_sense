import datetime
import json
from collections import defaultdict
from os import getenv

import psycopg2
from flask import Response

from connect import pg_connection

CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


class SensorData:
    def __init__(self, sensor_ids, temperature, moisture):
        self.sensor_ids = sensor_ids
        self.temperature = temperature
        self.moisture = moisture

    def post_data(self):
        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        try:
            with postgres_connection.cursor() as cur:
                insert = f"INSERT INTO sensor_data (sensor_id, temperature, moisture) values ({self.sensor_id}, {self.temperature}, {self.moisture});"
                cur.execute(insert)
                print(
                    f"Inserting {self.sensor_id}, {self.temperature}, {self.moisture}"
                )
            postgres_connection.commit()
            response = {"message": "success"}
            return Response(
                response=json.dumps(response), status=201, mimetype="application/json"
            )
        # TODO should handle failure on commit and send back appropriate status code
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()

    def get_data(self):
        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        try:
            with postgres_connection.cursor() as cur:
                query = f"SELECT * FROM sensor_data WHERE sensor_id IN ({self.sensor_ids}) AND created > now() - interval '{minutes} minutes';"
                cur.execute(query)
                results = cur.fetchall()

                # parse results into a better format for response
                response_data = defaultdict(list)
                for result in results:
                    date, sensor_id, temperature, moisture = result
                    date_string = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M")
                    response_data[sensor_id].append(
                        (date_string, temperature, moisture)
                    )
                response = {"message": "success", "data": response_data}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except:  # TODO add more specific exceptions
            response = {"message": "fail", "data": {}}
            return Response(
                response=json.dumps(response), status=418, mimetype="application/json"
            )
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()

    @staticmethod
    def bad_db_response():
        # TODO pass in response as argument
        response = {"message": "fail", "data": {}}
        return Response(
            response=json.dumps(response), status=503, mimetype="application/json"
        )
