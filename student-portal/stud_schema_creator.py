from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")

# Database connection parameters
db_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "student_portal",
    "user": "postgres",
    "password": PSQL_PASSWORD
}

# Pydantic model
class StudentApplication(BaseModel):
    application_id: Optional[str]
    student_name: str
    age: str
    gender: str
    course: str
    competitive_exam: str
    student_photo: Optional[bytes]
    marks_10: Optional[bytes]
    marks_12: Optional[bytes]
    exam_pdf: Optional[bytes]

class DepartmentInfo(BaseModel):
    course_name: str
    total_seats: int
    available_seats: int


# Function to create table if not exists
def create_table():
    # Query to create the student applications table
    create_student_applications_query = """
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
    );
    """
    
    # Query to create the department_info table
    create_department_info_query = """
    CREATE TABLE IF NOT EXISTS department_info (
        course_name TEXT PRIMARY KEY,
        total_seats INT NOT NULL,
        available_seats INT NOT NULL
    );
    """
    
    try:
        conn = psycopg2.connect(**db_params)
        with conn:
            with conn.cursor() as cur:
                # Create student applications table
                cur.execute(create_student_applications_query)
                # Create department info table
                cur.execute(create_department_info_query)
        print("Tables 'student_applications' and 'department_info' are ready.")
    except Exception as e:
        print("Error creating tables:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_table()
