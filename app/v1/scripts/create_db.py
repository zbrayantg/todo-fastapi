import psycopg2

from app.v1.utils.db import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


def create_db():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS
    )

    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"CREATE DATABASE {DB_NAME} WITH OWNER = {DB_USER} \
                ENCODING = 'UTF8' CONNECTION LIMIT = -1;"
        )
        print(f"Database {DB_NAME} created successfully")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {DB_NAME} already exists")

    cursor.close()
    conn.close()
