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


results = postgres_demo(None)
print(results)
