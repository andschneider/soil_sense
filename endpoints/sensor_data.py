import datetime
import json
from collections import defaultdict
from os import getenv

from flask import Response, request
from flask_restful import Resource

from utils.connect import pg_connection
from utils.db_execptions import bad_db_response

CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


class SensorData(Resource):
    def get(self):
        # parse arguments
        json_data = request.get_json()
        sensor_ids = json_data.get("sensor_ids")
        minutes = json_data.get("minutes")

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
        except Exception as e:
            return bad_db_response(e.args)
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()

    def post(self):
        request_json = request.get_json(silent=True)
        sensor_id = request_json.get("sensor_id", None)
        temperature = request_json.get("temperature", None)
        moisture = request_json.get("moisture", None)

        bad_params = [
            param[0]
            for param in [
                ("sensor_id", sensor_id),
                ("temperature", temperature),
                ("moisture", moisture),
            ]
            if param[1] is None
        ]
        if bad_params:
            response = {"message": f"{bad_params} were not supplied."}
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
        except Exception as e:
            return bad_db_response(e.args)
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()
