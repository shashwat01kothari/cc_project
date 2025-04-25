from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

class DepartmentInfo(BaseModel):
    course_name: str
    total_seats: int
    available_seats: int

class AppNumber(BaseModel):
    app_number:str

class StatusResponse(BaseModel):
    status: str

class StudentApplication(BaseModel):
    application_id: str
    competitive_exam: str
    status: bool

class DocumentInsertRequest(BaseModel):
    application_id: uuid.UUID
    student_name: str
    age: str
    gender: str
    course: str
    competitive_exam: str
    student_photo: str  # binary encoded as latin1
    marks_10: str       # binary encoded as latin1
    marks_12: str       # binary encoded as latin1
    exam_pdf: str       # binary encoded as latin1
    status: bool        # 'verified' or 'unverified'

class UpdateSeats(BaseModel):
    course_name : str

import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os

load_dotenv()

PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
db_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "admin_dashboard",
    "user": "postgres",
    "password": PSQL_PASSWORD
}


def update_seats(course_name:UpdateSeats):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE departments
        SET available_seats = available_seats - 1
        WHERE course_name = %s
    """, (course_name.course_name,))
    
    conn.commit()
    cursor.close()
    conn.close()

def create_tables():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    # Creating the 'departments' table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            course_name VARCHAR PRIMARY KEY,
            total_seats INT,
            available_seats INT
        );
    """)

    # Creating the 'student_applications' table
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
    

    cur.execute("""
                CREATE TABLE admissions_2025 (
                    application_id VARCHAR(255) PRIMARY KEY,
                    student_name VARCHAR(255) NOT NULL,
                    age INT NOT NULL,
                    course VARCHAR(255) NOT NULL,
                    competitive_exam BOOLEAN
                );
                """)
    conn.commit()
    cur.close()
    conn.close()

def get_seat_info():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT course_name, total_seats, available_seats FROM departments")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def student_applications():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT application_id, competitive_exam, status FROM student_applications WHERE status = false limit 5;")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def verify_student_application(application_id: str):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("""
        UPDATE student_applications
        SET status = true
        WHERE application_id = %s AND status = false
    """, (application_id,))
    conn.commit()
    cur.close()
    conn.close()

def insert_docs(data):
    try:
        conn = psycopg2.connect(**db_params)
        with conn:
            with conn.cursor() as cur:
                # Convert back to bytes
                photo_bytes = data.student_photo.encode("latin1")
                marks10_bytes = data.marks_10.encode("latin1")
                marks12_bytes = data.marks_12.encode("latin1")
                exam_pdf_bytes = data.exam_pdf.encode("latin1")

                # Insert data into student_applications table
                cur.execute("""
                    INSERT INTO student_applications (
                        application_id, student_name, age, gender, course,
                        competitive_exam, student_photo, marks_10, marks_12,
                        exam_pdf, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(data.application_id),
                    data.student_name,
                    data.age,
                    data.gender,
                    data.course,
                    data.competitive_exam,
                    photo_bytes,
                    marks10_bytes,
                    marks12_bytes,
                    exam_pdf_bytes,
                    data.status
                ))
    except Exception as e:
        print("Database error in insert_document_info:", e)
        raise HTTPException(status_code=500, detail="Failed to insert document info")
    finally:
        if conn:
            conn.close()

    return {"message": "Document info inserted successfully"}


async def get_verification_status(app_number: str):
    try:
        # Establish connection to the database
        app_uuid = uuid.UUID(app_number)
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Execute raw SQL query
        cur.execute("SELECT status FROM student_applications WHERE application_id = %s", (app_number,))

        # Fetch the result
        result = cur.fetchone()

        if result:
            # Return the status if found
            return StatusResponse(status=result[0])

        else:
            # Raise an error if the application is not found
            raise HTTPException(status_code=404, detail="Application not found")

    except Exception as e:
        # Handle any errors during the connection or query execution
        raise HTTPException(status_code=500, detail="Error fetching status: " + str(e))
    
    finally:
        # Close cursor and connection to release resources
        if cur:
            cur.close()
        if conn:
            conn.close()


def confirm_student_seat(app_number: str):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("""
            SELECT status
            FROM student_applications WHERE application_id = %s
        """, (app_number,))
        result = cur.fetchone()
        if result[0]==False or result[0]=='f':
            raise HTTPException(status_code=400, detail="Documents not verified yet")
        else :
            cur.execute("""
                SELECT application_id 
                FROM admissions_2025 
                WHERE application_id = %s
            """, (app_number,))
            result=cur.fetchone()
            if result is None :
                raise HTTPException(status_code=400, detail=f"Seat already confirmed with this application {app_number}")
        

        cur.execute("""
            SELECT application_id, student_name, age, course, competitive_exam
            FROM student_applications
            WHERE application_id = %s
        """, (app_number,))
        
        student_data = cur.fetchone()
        
        # If no data found, raise an error
        if not student_data:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Step 2: Insert the selected data into admissions_2025 table
        cur.execute("""
            INSERT INTO admissions_2025 (application_id, student_name, age, course, competitive_exam)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_data[0], student_data[1], student_data[2], student_data[3], student_data[4]))
        
        # Commit the changes to the database
        conn.commit()

        cur.close()
        conn.close()

        return {"message": f"Student seat for {app_number} confirmed"}

        
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database query failed: " + str(e))


if __name__ == "__main__":
    create_tables()


