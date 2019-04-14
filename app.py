from flask import Flask
from flask_restful import Api

from endpoints.sensor_info import SensorInfo
from endpoints.sensor_data import SensorData

app = Flask(__name__)
api = Api(app)


api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")
api.add_resource(SensorData, "/sensor_data")

if __name__ == "__main__":
    app.run(debug=True, port=3030)
