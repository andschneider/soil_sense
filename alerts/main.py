from api_calls import SensorAPI


def check_moisture(request):
    moisture_threshold = request.args.get("moisture")

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
            if moisture < moisture_threshold:
                # TODO send real alert
                print(f"Sensor {sensor_id} needs some water!")
        else:
            print(f"Sensor {sensor_id} seems to be offline!")

    return 200
