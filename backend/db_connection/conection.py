# db.py
import psycopg2
from psycopg2.extensions import connection
from typing import Generator
from dotenv import load_dotenv
import os

load_dotenv()
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
# Database connection parameters
db_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "cc_project",
    "user": "postgres",
    "password": PSQL_PASSWORD
}

def get_db() -> Generator[connection, None, None]:
    conn = psycopg2.connect(**db_params)
    try:
        yield conn
    finally:
        conn.close()
