import datetime

import jwt
from flask import current_app
from sqlalchemy.sql import func

from api import db, bcrypt


class SensorDataModel(db.Model):

    __tablename__ = "sensor_data"

    sensor_id = db.Column(db.Integer, nullable=False)
    created = db.Column(
        db.DateTime, default=func.now(), nullable=False, primary_key=True
    )
    temperature = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Integer, nullable=False)

    def __init__(self, sensor_id, temperature, moisture):
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.moisture = moisture


class SensorInfoModel(db.Model):

    __tablename__ = "sensor_info"

    sensor_id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated = db.Column(db.DateTime)
    plant = db.Column(db.String, default=True, nullable=False)

    def __init__(self, sensor_id, plant):
        self.sensor_id = sensor_id
        self.plant = plant


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode()
