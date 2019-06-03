import json

from flask import Response


def bad_db_response(exception):
    """Catch all exception return response."""
    response = {"message": "fail", "data": {"exception": exception}}
    return Response(
        response=json.dumps(response), status=503, mimetype="application/json"
    )
