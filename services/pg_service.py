# services/pg_service.py

import psycopg2
from config import POSTGRES_URI

# Connect to PostgreSQL
def connect_to_postgres():
    conn = psycopg2.connect(POSTGRES_URI)
    return conn

def insert_message(message):
    conn = connect_to_postgres()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO hello_table (message) VALUES (%s) RETURNING id;", (message,))
    inserted_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return inserted_id

def get_messages():
    conn = connect_to_postgres()
    cursor = conn.cursor()
    cursor.execute("SELECT id, message FROM hello_table;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": row[0], "message": row[1]} for row in rows]
