import json

from flask import Response, Blueprint
from flask_jwt_extended import jwt_required
from flask_restplus import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError

from api import db
from api.core.db_execptions import bad_db_response
from api.core.models import UserModel

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint, doc="/docs/")


@api.route("/users")
class Users(Resource):
    @jwt_required
    def post(self):
        """Create a user."""
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

        try:
            db.session.add(
                UserModel(username=args["username"], password=args["password"])
            )
            db.session.commit()
            response = {"message": "success"}
        except IntegrityError:
            db.session.rollback()
            response = {
                "message": f"User {args['username']} already exists in database."
            }
            return Response(
                response=json.dumps(response), status=409, mimetype="application/json"
            )
        return Response(
            response=json.dumps(response), status=201, mimetype="application/json"
        )

    @jwt_required
    def delete(self):
        """Deletes a user."""
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        args = parser.parse_args()

        # TODO need to handle deleting an entry that doesn't exist
        try:
            sensor_info = (
                db.session.query(UserModel).filter_by(username=args["username"]).first()
            )
            db.session.delete(sensor_info)
            db.session.commit()

            response = {"message": f"User {args['username']} successfully deleted"}
            return Response(
                response=json.dumps(response), status=200, mimetype="application/json"
            )
        except Exception as e:
            return bad_db_response(e.args)
