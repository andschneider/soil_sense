from datetime import datetime, timedelta
import json
from collections import defaultdict

from flask import Response, request, Blueprint
from flask_jwt_extended import jwt_required
from flask_restplus import Api, Namespace, Resource, reqparse

from api import db
from api.core.db_execptions import bad_db_response
from api.core.models import SensorDataModel


api = Namespace("sensor_data", description="GET and POST for sensor readings.")

get_args = reqparse.RequestParser()
get_args.add_argument("sensor_ids", action="split", required=True)
get_args.add_argument("minutes", type=int, required=True)

post_args = reqparse.RequestParser()
post_args.add_argument("sensor_id", type=int, required=True)
post_args.add_argument("temperature", type=float, required=True)
post_args.add_argument("moisture", type=int, required=True)


@api.route("/sensor_data")
class SensorData(Resource):
    @jwt_required
    @api.expect(get_args)
    def get(self):
        """Get sensor readings for a list of sensor_ids and X amount of minutes."""
        # parse arguments
        args = get_args.parse_args()

        now = datetime.utcnow()
        filter_time = now - timedelta(minutes=args["minutes"])

        try:
            # filter by id and minutes of data
            query = SensorDataModel.query.filter(
                SensorDataModel.sensor_id.in_(args["sensor_ids"]),
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

    @jwt_required
    @api.expect(post_args)
    def post(self):
        """Create a new record for a sensor reading."""
        args = post_args.parse_args()

        try:
            sensor_data = SensorDataModel(
                sensor_id=args["sensor_id"],
                temperature=args["temperature"],
                moisture=args["moisture"],
            )
            db.session.add(sensor_data)
            db.session.commit()
            response = {"message": "success"}
            return Response(
                response=json.dumps(response), status=201, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)
