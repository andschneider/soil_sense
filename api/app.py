from flask.cli import FlaskGroup
from sqlalchemy.exc import IntegrityError

from api import create_app, db
from api.core.models import SensorInfoModel, UserModel

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    try:
        db.session.add(SensorInfoModel(sensor_id=1, plant="Monstera", alert_level=500))
        db.session.add(UserModel(username="andrew", password="password"))
        db.session.commit()
    except IntegrityError:
        print("Seed data already exists in db!")


if __name__ == "__main__":
    cli()
