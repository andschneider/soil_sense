import json

from flask import Response, Blueprint
from flask_restful import Resource, Api

from api import db
from api.core.db_execptions import bad_db_response
from api.core.models import SensorDataModel


sensor_ids_blueprint = Blueprint("sensor_ids", __name__)
api = Api(sensor_ids_blueprint)


class SensorIds(Resource):
    def get(self):
        """Gets the unique sensor id's."""
        try:
            query = db.session.query(
                SensorDataModel.sensor_id.distinct().label("sensor_id")
            )
            id_list = [row.sensor_id for row in query.all()]
            response = {"message": "success", "sensor_ids": id_list}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)


api.add_resource(SensorIds, "/sensor_ids")
