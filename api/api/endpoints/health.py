import json

from flask import Response, Blueprint
from flask_restplus import Api, Namespace, Resource

from api import db
from api.core.db_execptions import bad_db_response
from api.core.models import SensorDataModel


api = Namespace("health", description="Healthchecks.")


@api.route("/health")
@api.doc(security=None)
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
