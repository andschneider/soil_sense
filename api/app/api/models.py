from sqlalchemy.sql import func

from app import db


class SensorData(db.Model):

    __tablename__ = "sensor_data"

    sensor_id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
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
