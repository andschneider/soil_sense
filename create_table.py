from os import getenv

from connect import pg_connection

CONNECTION_NAME = getenv("INSTANCE_CONNECTION_NAME")


def create_table():
    command = """CREATE TABLE sensor_data (
                    created timestamp DEFAULT current_timestamp,
                    sensor_id integer NOT NULL, 
                    temperature float NOT NULL,  
                    moisture integer NOT NULL 
                 );"""
    conn = pg_connection(f"/cloudsql/{CONNECTION_NAME}")

    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("table created")
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    create_table()
