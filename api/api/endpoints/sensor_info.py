import datetime
import json

import psycopg2
from flask import Response, request, Blueprint
from flask_restful import Resource, Api

from api.core.db_execptions import bad_db_response
from api.core.models import SensorInfoModel

sensor_info_blueprint = Blueprint("sensor_info", __name__)
api = Api(sensor_info_blueprint)


class SensorInfo(Resource):
    def get(self, sensor_id):
        try:
            sensor_info = SensorInfoModel.query.filter_by(sensor_id=sensor_id).first()
            response = {
                "message": "success",
                "data": {
                    "sensor_id": sensor_info.sensor_id,
                    "plant_name": sensor_info.plant,
                },
            }
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)

    def post(self, sensor_id):
        # parse arguments
        json_data = request.get_json()
        plant_name = json_data.get("plant")

        postgres_connection = pg_connection(f"/cloudsql/{CONNECTION_NAME}")
        try:
            with postgres_connection.cursor() as cur:
                insert = "INSERT INTO sensor_info (sensor_id, plant) values (%s, %s);"
                cur.execute(insert, (sensor_id, plant_name))
                print(f"Inserting {sensor_id}, {plant_name}")
            postgres_connection.commit()

            response = {"message": "success"}
            return Response(
                response=json.dumps(response), status=201, mimetype="application/json"
            )
        except psycopg2.errors.UniqueViolation:
            response = {
                "message": f"Sensor id {sensor_id} already exists in database. Try updating or deleting first."
            }
            return Response(
                response=json.dumps(response), status=409, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()

    def put(self, sensor_id):
        # parse arguments
        json_data = request.get_json()
        plant_name = json_data.get("plant")

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
        except Exception as e:
            return bad_db_response(e.args)
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
        except Exception as e:
            return bad_db_response(e.args)
        finally:
            if postgres_connection:
                cur.close()
                postgres_connection.close()


api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")
