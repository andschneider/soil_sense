import datetime
import json
from os import getenv

import psycopg2
from flask import Response, request
from flask_restful import Resource
from flask_restful import reqparse

from utils.connect import pg_connection

CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


class SensorInfo(Resource):
    def get(self, sensor_id):
        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        try:
            with postgres_connection.cursor() as cur:
                query = "SELECT * FROM sensor_info WHERE sensor_id = %s;"
                cur.execute(query, (sensor_id,))
                results = cur.fetchone()
                created = results[0]
                updated = results[1]
                sensor_id_query = results[2]
                plant_name = results[3]
                # TODO add the created and updated to the response?
                response = {
                    "message": "success",
                    "data": {"sensor_id": sensor_id_query, "plant_name": plant_name},
                }
                return Response(
                    response=json.dumps(response),
                    status=200,
                    mimetype="application/json",
                )
        except:  # TODO add more specific exceptions
            return self.bad_db_response()
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()

    def post(self, sensor_id):
        # parse arguments
        plant_name = request.args.get("plant")
        # parser = reqparse.RequestParser()
        # parser.add_argument("plant", type=str, required=True)
        # args = parser.parse_args()
        # plant_name = args.get("plant")

        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        try:
            with postgres_connection.cursor() as cur:
                insert = "INSERT INTO Sensor_info (sensor_id, plant) values (%s, %s);"
                cur.execute(insert, (sensor_id, plant_name))
                print(f"Inserting {sensor_id}, {plant_name}")
            postgres_connection.commit()

            response = {"message": "success"}
            return Response(
                response=json.dumps(response), status=201, mimetype="application/json"
            )
        except psycopg2.IntegrityError as e:
            response = {
                "message": f"sensor id {self.sensor_id} already exists in database. Try updating or deleting first."
            }
            return Response(
                response=json.dumps(response), status=409, mimetype="application/json"
            )
        except:
            return self.bad_db_response()
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()

    def put(self, sensor_id):
        # parse arguments
        plant_name = request.args.get("plant")
        # parser = reqparse.RequestParser()
        # parser.add_argument("plant", type=str, required=True)
        # args = parser.parse_args()
        # plant_name = args.get("plant")

        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        # TODO this seems to return 200 if updating a sensor that doesn't exist
        now = datetime.datetime.utcnow()
        try:
            with postgres_connection.cursor() as cur:
                update = "UPDATE sensor_info SET plant = %s, updated = %s WHERE sensor_id = %s;"
                cur.execute(update, (plant_name, now, sensor_id))
            postgres_connection.commit()
            response = {"message": f"Sensor id {sensor_id} successfully updated"}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except:
            return self.bad_db_response()
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()

    def delete(self, sensor_id):
        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        # TODO this seems to return 200 if deleting a sensor that doesn't exist
        try:
            with postgres_connection.cursor() as cur:
                update = "DELETE FROM sensor_info WHERE sensor_id = %s;"
                cur.execute(update, (sensor_id,))
            postgres_connection.commit()

            response = {"message": f"Sensor id {sensor_id} successfully deleted"}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except:
            return self.bad_db_response()
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
