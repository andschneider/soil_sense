import pytest

from flask_sqlalchemy import SQLAlchemy

from api import create_app

db = SQLAlchemy()


@pytest.fixture(scope="module")
def client():
    app = create_app()

    db.init_app(app)

    client = app.test_client()

    yield client


@pytest.fixture(scope="module")
def token(client):
    api_prefix = "/api/v1"
    data = {"username": "andrew", "password": "password"}
    response = client.post(api_prefix + "/auth", json=data)
    message = response.get_json()
    return "Bearer " + message["auth_token"]
