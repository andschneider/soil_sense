import json

from flask import Response

from api_calls import SensorAPI


def check_moisture(request):
    moisture_threshold = request.args.get("moisture")

    if moisture_threshold is None:
        response = {"message": "moisture value must be supplied"}
        return Response(
            response=json.dumps(response), status=400, mimetype="application/json"
        )

    api = SensorAPI()

    # get available sensor ids
    status, sensor_ids = api.get_sensor_ids()

    if status != 200:
        # TODO add some error handling
        print("Could not get sensor ids")

    # check the data for the sensor ids
    sensor_data = api.get_sensor_data(minutes=10, sensor_ids=sensor_ids["sensor_ids"])

    for sensor_id in sensor_ids["sensor_ids"]:
        sensor_data_id = sensor_data["data"].get(str(sensor_id))
        if sensor_data_id:
            data = sensor_data_id[-1]
            moisture = data[-1]
            if moisture < int(moisture_threshold):
                # TODO send real alert
                print(f"Sensor {sensor_id} needs some water!")
        else:
            print(f"Sensor {sensor_id} seems to be offline!")

    response = {"message": "alert completed successfully"}
    return Response(
        response=json.dumps(response), status=200, mimetype="application/json"
    )
