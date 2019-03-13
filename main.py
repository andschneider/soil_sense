import datetime
from collections import defaultdict
from os import getenv

from flask import jsonify

from connect import pg_connection
from sensor_info import SensorInfo


CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


def get_sensor_data(request):
    # parse request data
    sensor_ids = request.args.get("sensor_ids", 1)
    minutes = request.args.get("minutes", 10)

    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    try:
        with conn.cursor() as cur:
            # TODO make this actually date based, not just using LIMIT
            query = f"SELECT * FROM sensor_data WHERE sensor_id IN ({sensor_ids}) ORDER BY created DESC LIMIT {minutes};"
            cur.execute(query)
            results = cur.fetchall()

            # parse results into a better format for response
            response_data = defaultdict(list)
            for result in results:
                date, sensor_id, temperature, moisture = result
                date_string = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M")
                response_data[sensor_id].append((date_string, temperature, moisture))
            response = {"message": "success", "data": response_data}
        return jsonify(response), 200
    except:  # TODO add more specific exceptions
        response = {"message": "fail", "data": {}}
        return jsonify(response), 418
    finally:
        if conn:
            cur.close()
            conn.close()


def get_sensor_ids(request):
    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    try:
        with conn.cursor() as cur:
            query = "SELECT DISTINCT sensor_id FROM sensor_data;"
            cur.execute(query)
            results = cur.fetchall()

            # parse results and format response
            id_list = []
            for sensor_id in results:
                # results of the distinct query are single tuples, e.g. (1,)
                id_list.append(sensor_id[0])
            response = {"message": "success", "sensor_ids": id_list}
            return jsonify(response), 200
    except:  # TODO add more specific exceptions
        response = {"message": "fail", "sensor_ids": []}
        return jsonify(response), 418
    finally:
        if conn:
            cur.close()
            conn.close()


def insert_data(request):
    # parse request data
    request_json = request.get_json(silent=True)

    if request_json:
        sensor_id = request_json.get("sensor_id", None)
        temperature = request_json.get("temperature", None)
        moisture = request_json.get("moisture", None)

    if None in [sensor_id, temperature, moisture]:
        # TODO send back a more useful message
        return jsonify({"message": "fail"}), 400

    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    try:
        with conn.cursor() as cur:
            insert = f"INSERT INTO sensor_data (sensor_id, temperature, moisture) values ({sensor_id}, {temperature}, {moisture});"
            cur.execute(insert)
            print(f"Inserting {sensor_id}, {temperature}, {moisture}")
        conn.commit()
        return jsonify({"message": "success"}), 201
    # TODO should handle failure on commit and send back appropriate status code
    finally:
        if conn:
            cur.close()
            conn.close()


def insert_sensor_info(request):
    # parse request data
    request_json = request.get_json(silent=True)

    if request_json:
        sensor_id = request_json.get("sensor_id", None)
        plant_name = request_json.get("plant", None)

    if None in [sensor_id, plant_name]:
        # TODO send back a more useful message
        return jsonify({"message": "fail"}), 400

    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    sensor = SensorInfo(conn, sensor_id, plant_name)
    return sensor.post_data()


def get_sensor_info(request):
    # parse request data
    sensor_id = request.args.get("sensor_id", None)

    if sensor_id is None:
        # TODO send back a more useful message
        return jsonify({"message": "fail"}), 400

    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    sensor = SensorInfo(conn, sensor_id, None)
    return sensor.get_data()


def update_sensor_info(request):
    # parse request data
    request_json = request.get_json(silent=True)

    if request_json:
        sensor_id = request_json.get("sensor_id", None)
        plant_name = request_json.get("plant", None)

    if None in [sensor_id, plant_name]:
        # TODO send back a more useful message
        return jsonify({"message": "fail"}), 400

    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    sensor = SensorInfo(conn, sensor_id, plant_name)
    return sensor.update_data()


def delete_sensor_info(request):
    # parse request data
    request_json = request.get_json(silent=True)

    if request_json:
        sensor_id = request_json.get("sensor_id", None)

    if sensor_id is None:
        # TODO send back a more useful message
        return jsonify({"message": "fail"}), 400

    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    sensor = SensorInfo(conn, sensor_id, None)
    return sensor.delete_data()
