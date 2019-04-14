from flask import Flask
from flask_restful import Api

from endpoints.sensor_info import SensorInfo

app = Flask(__name__)
api = Api(app)


api.add_resource(SensorInfo, "/sensor_info/<int:sensor_id>")

if __name__ == "__main__":
    app.run(debug=True, port=3030)
