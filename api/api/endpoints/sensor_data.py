from datetime import datetime, timedelta
import json
from collections import defaultdict

from flask import Response, request, Blueprint
from flask_restful import Resource, Api

from api import db
from api.core.db_execptions import bad_db_response
from api.core.models import SensorDataModel

sensor_data_blueprint = Blueprint("sensor_data", __name__)
api = Api(sensor_data_blueprint)


class SensorData(Resource):
    def get(self):
        # parse arguments
        sensor_ids = request.args.get("sensor_ids")
        minutes = request.args.get("minutes")

        now = datetime.utcnow()
        filter_time = now - timedelta(minutes=int(minutes))

        try:
            # filter by id and minutes of data
            query = SensorDataModel.query.filter(
                SensorDataModel.sensor_id.in_(
                    (sensor_id for sensor_id in sensor_ids.split(","))
                ),
                SensorDataModel.created > filter_time,
            )

            response_data = defaultdict(list)
            for result in query.all():
                date_string = datetime.strftime(result.created, "%Y-%m-%d %H:%M")
                response_data[result.sensor_id].append(
                    (date_string, result.temperature, result.moisture)
                )

            response = {"message": "success", "data": response_data}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)

    def post(self):
        request_json = request.get_json(silent=True)
        sensor_id = request_json.get("sensor_id", None)
        temperature = request_json.get("temperature", None)
        moisture = request_json.get("moisture", None)

        # TODO replace this argument parsing with something legit
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

        try:
            sensor_data = SensorDataModel(
                sensor_id=sensor_id, temperature=temperature, moisture=moisture
            )
            db.session.add(sensor_data)
            db.session.commit()
            response = {"message": "success"}
            return Response(
                response=json.dumps(response), status=201, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)


api.add_resource(SensorData, "/sensor_data")
