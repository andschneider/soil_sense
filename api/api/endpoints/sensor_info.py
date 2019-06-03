import datetime
import json

from flask import Response, request, Blueprint
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError

from api.core.db_execptions import bad_db_response
from api.core.models import SensorInfoModel

from api import db


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

        try:
            sensor_info = SensorInfoModel(sensor_id=sensor_id, plant=plant_name)
            db.session.add(sensor_info)
            db.session.commit()
            response = {"message": "success"}
            return Response(
                response=json.dumps(response), status=201, mimetype="application/json"
            )
        except IntegrityError:
            response = {
                "message": f"Sensor id {sensor_id} already exists in database. Try updating or deleting first."
            }
            return Response(
                response=json.dumps(response), status=409, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)

    def put(self, sensor_id):
        # parse arguments
        json_data = request.get_json()
        plant_name = json_data.get("plant")

        now = datetime.datetime.utcnow()
        sensor_info = SensorInfoModel.query.filter_by(sensor_id=sensor_id).first()

        if sensor_info:
            try:
                sensor_info.plant = plant_name
                sensor_info.updated = now
                db.session.commit()

                response = {"message": f"Sensor id {sensor_id} successfully updated"}
                return Response(
                    response=json.dumps(response),
                    status=200,
                    mimetype="application/json",
                )
            except Exception as e:
                return bad_db_response(e.args)
        # TODO handle updating entry that doesn't exist

    def delete(self, sensor_id):
        # TODO need to handle deleting an entry that doesn't exist
        try:
            sensor_info = (
                db.session.query(SensorInfoModel).filter_by(sensor_id=sensor_id).first()
            )
            db.session.delete(sensor_info)
            db.session.commit()

            response = {"message": f"Sensor id {sensor_id} successfully deleted"}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)


api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")
