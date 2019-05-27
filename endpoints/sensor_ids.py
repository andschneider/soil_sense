import json
from os import getenv

from flask import Response
from flask_restful import Resource

from utils.connect import pg_connection
from utils.db_execptions import bad_db_response

CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


class SensorIds(Resource):
    def get(self):
        conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

        try:
            with conn.cursor() as cur:
                query = "SELECT DISTINCT sensor_id FROM sensor_data;"
                cur.execute(query)
                results = cur.fetchall()

                # results of the distinct query are single tuples, e.g. (1,)
                id_list = [sensor_id[0] for sensor_id in results]
                response = {"message": "success", "sensor_ids": id_list}
                return Response(
                    response=json.dumps(response),
                    status=200,
                    mimetype="application/json",
                )
        except Exception as e:
            return bad_db_response(e.args)
        finally:
            if conn:
                cur.close()
                conn.close()
