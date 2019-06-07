import json

from flask import Response, Blueprint
from flask_restplus import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError

from api import db
from api.core.models import UserModel

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint, doc="/docs/")


@api.route("/users")
class Users(Resource):
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
