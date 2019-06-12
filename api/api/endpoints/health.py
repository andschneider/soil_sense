import json

from flask import Response, Blueprint
from flask_restplus import Api, Resource

from api import db
from api.core.db_execptions import bad_db_response
from api.core.models import SensorDataModel


health_blueprint = Blueprint("health", __name__)
api = Api(health_blueprint, doc="/docs/")


@api.route("/health")
class SensorIds(Resource):
    def get(self):
        """Simple health check endpoint"""
        try:
            # TODO is there a better way to check connection to the db?
            query = db.session.query(
                SensorDataModel.sensor_id.distinct().label("sensor_id")
            )
            response = {"message": "success"}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)
