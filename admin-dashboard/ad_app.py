#port 8002


from fastapi import FastAPI, HTTPException, Query
from ad_schema_creator import AppNumber, DepartmentInfo, DocumentInsertRequest, StatusResponse, StudentApplication , UpdateSeats, confirm_student_seat ,get_seat_info, get_verification_status, insert_docs, student_applications, verify_student_application ,update_seats
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Generator, List, Optional
from uuid import uuid4
import psycopg2
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")


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



@app.get("/api/seatInfo")
def get_seat_information():
    data = get_seat_info()
    return [DepartmentInfo(course_name=dept[0], total_seats=dept[1], available_seats=dept[2]) for dept in data]

@app.get("/api/studentApplications", response_model=List[StudentApplication])
def get_student_applications():
    try:
        # Fetch student applications with or without the application_id filter
        data = student_applications()

        # Return the applications as a list of Pydantic models
        return [
            StudentApplication(application_id=app[0], competitive_exam=app[1], status=app[2])
            for app in data
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@app.put("/api/updateSeatInfo")
def update_seats_info(course_name:UpdateSeats):
    update_seats(course_name=course_name)

@app.put("/api/studentApplications/verify/{application_id}")
async def verify_application(application_id: str):
    verify_student_application(application_id)
    

@app.post("/api/updateDocumentInfo")
async def insert_document_info(data: DocumentInsertRequest):
    insert_docs(data)

@app.get("/api/getStatus/{app_number}",response_model=StatusResponse)
async def get_status(app_number: str):
    status=await get_verification_status(app_number)

    return status

