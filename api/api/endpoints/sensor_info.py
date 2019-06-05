import datetime
import json

from flask import Response, request, Blueprint
from flask_restplus import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError

from api.core.db_execptions import bad_db_response
from api.core.models import SensorInfoModel

from api import db


sensor_info_blueprint = Blueprint("sensor_info", __name__)
api = Api(sensor_info_blueprint, doc="/docs/")


@api.route("/sensor_info/<int:sensor_id>")
class SensorInfo(Resource):
    def get(self, sensor_id):
        """Get sensor info for a given sensor_id."""
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
        """Creates a new sensor info entry."""
        parser = reqparse.RequestParser()
        parser.add_argument("plant", type=str, required=True)
        args = parser.parse_args()

        try:
            sensor_info = SensorInfoModel(sensor_id=sensor_id, plant=args["plant"])
            db.session.add(sensor_info)
            db.session.commit()
            response = {"message": "success"}
        except IntegrityError:
            response = {
                "message": f"Sensor id {sensor_id} already exists in database. Try updating or deleting first."
            }
            return Response(
                response=json.dumps(response), status=409, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)

        return Response(
            response=json.dumps(response), status=201, mimetype="application/json"
        )

    def put(self, sensor_id):
        """Updates a sensor info entry."""
        parser = reqparse.RequestParser()
        parser.add_argument("plant", type=str, required=True)
        args = parser.parse_args()

        now = datetime.datetime.utcnow()
        sensor_info = SensorInfoModel.query.filter_by(sensor_id=sensor_id).first()

        if sensor_info:
            try:
                sensor_info.plant = args["plant"]
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
        """Deletes a sensor info entry."""
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
