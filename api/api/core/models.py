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

    def to_json(self):
        return {"id": self.id, "username": self.username}

    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(
                payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token"""
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
