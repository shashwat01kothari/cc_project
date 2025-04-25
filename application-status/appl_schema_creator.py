# schemas
from pydantic import BaseModel
from typing import Optional

class StudentInfo(BaseModel):
    studentName: str
    age: str
    gender: str
    competitiveExam: str
    documentVerificationStatus: str

class AppTracking(BaseModel):
    application_id: str
    student_name: str
    age: int
    course: str
    competitive_exam: str
    status: bool


# db_model
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os

load_dotenv()

PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
db_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "application_status",
    "user": "postgres",
    "password": PSQL_PASSWORD
}

def create_table():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_applications (
            application_id UUID PRIMARY KEY,
            student_name TEXT NOT NULL,
            age TEXT NOT NULL,
            gender TEXT NOT NULL,
            course TEXT NOT NULL,
            competitive_exam TEXT NOT NULL,
            student_photo BYTEA,
            marks_10 BYTEA,
            marks_12 BYTEA,
            exam_pdf BYTEA
            status BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.execte("""
    CREATE TABLE IF NOT EXISTS application_tracking (
    application_id UUID PRIMARY KEY,
    student_name TEXT NOT NULL,
    age INT NOT NULL,
    course TEXT NOT NULL,
    competitive_exam TEXT NOT NULL,
    status BOOLEAN DEFAULT FALSE
    );

    """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()