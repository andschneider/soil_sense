import datetime
import json
from collections import defaultdict
from os import getenv

from flask import Response, request
from flask_restful import Resource

from utils.connect import pg_connection

CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


class SensorData(Resource):
    def get(self):
        # parse arguments
        sensor_ids = request.args.get("sensor_ids")
        minutes = request.args.get("minutes")

        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        try:
            with postgres_connection.cursor() as cur:
                query = "SELECT * FROM sensor_data WHERE sensor_id IN %s AND created > now() - interval '%s minutes';"
                cur.execute(query, (tuple(sensor_ids.split(",")), int(minutes)))
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

    def post(self):
        request_json = request.get_json(silent=True)

        if request_json:
            sensor_id = request_json.get("sensor_id", None)
            temperature = request_json.get("temperature", None)
            moisture = request_json.get("moisture", None)

        if None in [sensor_id, temperature, moisture]:
            # TODO send back a more useful message
            response = {"message": "fail"}
            return Response(
                response=json.dumps(response), status=400, mimetype="application/json"
            )

        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        try:
            with postgres_connection.cursor() as cur:
                insert = f"INSERT INTO sensor_data (sensor_id, temperature, moisture) values ({sensor_id},{temperature},{moisture});"
                cur.execute(insert)
                print(f"Inserting {sensor_id}, {temperature}, {moisture}")
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

    @staticmethod
    def bad_db_response():
        # TODO pass in response as argument
        response = {"message": "fail", "data": {}}
        return Response(
            response=json.dumps(response), status=503, mimetype="application/json"
        )
