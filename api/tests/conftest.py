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
