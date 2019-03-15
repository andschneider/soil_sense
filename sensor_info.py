import datetime
import json

import psycopg2
from flask import jsonify, Response


class SensorInfo:
    def __init__(self, postgres_connection, sensor_id, plant_name):
        self.pg_con = postgres_connection
        self.sensor_id = sensor_id
        self.plant_name = plant_name

    def post_data(self):
        try:
            with self.pg_con.cursor() as cur:
                insert = "INSERT INTO Sensor_info (sensor_id, plant) values (%s, %s);"
                cur.execute(insert, (self.sensor_id, self.plant_name))
                print(f"Inserting {self.sensor_id}, {self.plant_name}")
            self.pg_con.commit()
            return jsonify({"message": "success"}), 201
        except psycopg2.IntegrityError as e:
            return (
                jsonify(
                    {
                        "message": f"sensor id {self.sensor_id} already exists in database. Try updating or deleting first."
                    }
                ),
                409,
            )
        except:
            # TODO add a more descriptive exception and a better response message
            return jsonify({"message": "fail"}), 503
        finally:
            if self.pg_con:
                cur.close()
                self.pg_con.close()

    def get_data(self):
        try:
            with self.pg_con.cursor() as cur:
                query = "SELECT * FROM sensor_info WHERE sensor_id = %s;"
                cur.execute(query, (self.sensor_id,))
                results = cur.fetchone()
                created = results[0]
                updated = results[1]
                sensor_id = results[2]
                plant_name = results[3]
                # TODO add the created and updated to the response?
                response = {
                    "message": "success",
                    "data": {"sensor_id": sensor_id, "plant_name": plant_name},
                }
                return Response(
                    response=json.dumps(response),
                    status=200,
                    mimetype="application/json",
                )
        except:  # TODO add more specific exceptions
            response = {"message": "fail", "data": {}}
            return Response(
                response=json.dumps(response), status=503, mimetype="application/json"
            )
        finally:
            if self.pg_con:
                cur.close()
                self.pg_con.close()

    def update_data(self):
        # TODO this seems to return 200 if updating a sensor that doesn't exist
        now = datetime.datetime.utcnow()
        try:
            with self.pg_con.cursor() as cur:
                update = "UPDATE sensor_info SET plant = %s, updated = %s WHERE sensor_id = %s;"
                cur.execute(update, (self.plant_name, now, self.sensor_id))
            self.pg_con.commit()
            return (
                jsonify(
                    {"message": f"Sensor id {self.sensor_id} successfully updated"}
                ),
                200,
            )
        except:
            # TODO add a more descriptive exception and a better response message
            return jsonify({"message": "fail"}), 503
        finally:
            if self.pg_con:
                cur.close()
                self.pg_con.close()

    def delete_data(self):
        # TODO this seems to return 200 if deleting a sensor that doesn't exist
        try:
            with self.pg_con.cursor() as cur:
                update = "DELETE FROM sensor_info WHERE sensor_id = %s;"
                cur.execute(update, (self.sensor_id,))
            self.pg_con.commit()
            return (
                jsonify(
                    {"message": f"Sensor id {self.sensor_id} successfully deleted"}
                ),
                200,
            )
        except:
            # TODO add a more descriptive exception and a better response message
            return jsonify({"message": "fail"}), 503
        finally:
            if self.pg_con:
                cur.close()
                self.pg_con.close()
