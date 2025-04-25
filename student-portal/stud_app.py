#port 8000


from fastapi import FastAPI, UploadFile, File, Form, params
from fastapi.middleware.cors import CORSMiddleware
from typing import Generator
from uuid import uuid4
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os
import httpx

# Load environment variables
load_dotenv()
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")

# PostgreSQL connection params
db_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "student_portal",
    "user": "postgres",
    "password": PSQL_PASSWORD
}

# DB dependency
def get_db() -> Generator[connection, None, None]:
    conn = psycopg2.connect(**db_params)
    try:
        yield conn
    finally:
        conn.close()

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from uuid import uuid4
import psycopg2
from psycopg2.extensions import connection

@app.post("/api/studentPortal")
async def submit_student_portal(
    studentName: str = Form(...),
    age: str = Form(...),
    gender: str = Form(...),
    course: str = Form(...),
    competitiveExam: str = Form(...),
    studentPhoto: UploadFile = File(...),
    marks10: UploadFile = File(...),
    marks12: UploadFile = File(...),
    examPdf: UploadFile = File(...),
):
    application_id = str(uuid4())

    # Check available seats in the department_info table
    try:
        conn = psycopg2.connect(**db_params)
        with conn:
            with conn.cursor() as cur:
                # Query to fetch available seats for the given course
                cur.execute("""
                    SELECT available_seats FROM department_info WHERE course_name = %s
                """, (course,))
                result = cur.fetchone()

                if not result:
                    raise HTTPException(status_code=404, detail="Course not found")
                
                available_seats = result[0]
                
                # Check if there are no available seats
                if available_seats == 0:
                    raise HTTPException(status_code=400, detail="No available seats for this course")

                # Proceed with inserting the application if seats are available
                photo_bytes = await studentPhoto.read()
                marks10_bytes = await marks10.read()
                marks12_bytes = await marks12.read()
                exam_pdf_bytes = await examPdf.read()

                # Insert the student application into the database
                cur.execute("""
                    INSERT INTO student_applications (
                        application_id, student_name, age, gender, course, competitive_exam,
                        student_photo, marks_10, marks_12, exam_pdf
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    application_id,
                    studentName,
                    age,
                    gender,
                    course,
                    competitiveExam,
                    photo_bytes,
                    marks10_bytes,
                    marks12_bytes,
                    exam_pdf_bytes
                ))
                # Update the available seats after a successful application
                cur.execute("""
                    UPDATE department_info SET available_seats = available_seats - 1 WHERE course_name = %s
                """, (course,))
                
    except Exception as e:
        print("DB Error:", e)
        return {"error": "Failed to save student application"}
    finally:
        if conn:
            conn.close()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put("http://127.0.0.1:8002/api/updateSeatInfo", 
                                        json={"course_name": course}
                                        )
            if response.status_code != 200:
                print("Warning: updateSeatInfo failed:", response.text)
    except Exception as e:
        print("Error calling updateSeatInfo:", e)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8002/api/updateDocumentInfo", 
                                        json={
                                        "application_id": application_id,
                                        "student_name": studentName,
                                        "age": age,
                                        "gender": gender,
                                        "course": course,
                                        "competitive_exam": competitiveExam,
                                        "student_photo": photo_bytes.decode("latin1"),
                                        "marks_10": marks10_bytes.decode("latin1"),
                                        "marks_12": marks12_bytes.decode("latin1"),
                                        "exam_pdf": exam_pdf_bytes.decode("latin1"),
                                        "status": False
                                    })
            if response.status_code != 200:
                print("Warning: updateSeatInfo failed:", response.text)
    except Exception as e:
        print("Error calling updateSeatInfo:", e)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8001/api/addAppTracking", 
                                        json={
                                        "application_id": application_id,
                                        "student_name": studentName,
                                        "age": age,
                                        "course": course,
                                        "competitive_exam": competitiveExam,
                                        "status": False
                                    })
            if response.status_code != 200:
                print("Warning: updateSeatInfo failed:", response.text)
    except Exception as e:
        print("Error calling updateSeatInfo:", e)


    return {"message": "Application submitted", "application_id": application_id}

