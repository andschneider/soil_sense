from os import getenv

from connect import pg_connection

CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


def postgres_demo(request):
    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    try:
        with conn.cursor() as cur:
            query = "select * from guestbook"
            cur.execute(query)
            results = cur.fetchall()
            return str(results)
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
        pass
        # TODO should send back a 400 or something

    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    try:
        with conn.cursor() as cur:
            insert = f"INSERT INTO sensor_data (sensor_id, temperature, moisture) values ({sensor_id}, {temperature}, {moisture});"
            cur.execute(insert)
            print(f"Inserting {sensor_id}, {temperature}, {moisture}")
        conn.commit()
        # TODO should send back a 201
    # TODO should handle failure on commit and send back appropriate status code
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    results = postgres_demo(None)
    print(results)
