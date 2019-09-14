import json

from flask import Blueprint, Response
from flask_jwt_extended import create_access_token
from flask_restplus import reqparse, Api, Namespace, Resource

from api import bcrypt
from api.core.db_execptions import bad_db_response
from api.core.models import UserModel


api = Namespace("auth", description="Authentication and users.")

parser = reqparse.RequestParser()
parser.add_argument("username", type=str, required=True)
parser.add_argument("password", type=str, required=True)


@api.route("/auth")
@api.doc(security=None)
@api.expect(parser)
class Auth(Resource):
    def post(self):
        """Create an authentication token."""
        args = parser.parse_args()

        try:
            user = UserModel.query.filter_by(username=args["username"]).first()
            if user and bcrypt.check_password_hash(user.password, args["password"]):
                # create token based on username
                access_token = create_access_token(identity=args["username"])
                response = {
                    "message": "Successfully logged in.",
                    "auth_token": access_token,
                }
                return Response(
                    response=json.dumps(response),
                    status=200,
                    mimetype="application/json",
                )

            else:
                response = {"message": "User does not exist."}
                return Response(
                    response=json.dumps(response),
                    status=400,
                    mimetype="application/json",
                )
        except Exception as e:
            return bad_db_response(e.args)
