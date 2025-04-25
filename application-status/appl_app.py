#port 8001

# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv
from appl_schema_creator import AppTracking
import httpx

load_dotenv()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
db_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "application_status",
    "user": "postgres",
    "password": PSQL_PASSWORD
}

@app.get("/api/getData", response_model=str)
async def get_data(app_number: str):
    try:
        # Send a request to the external server to fetch the status
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8002/api/getStatus/{app_number}")
            
            if response.status_code == 200:
                status_from_server = response.json().get("status")
                if status_from_server:
                    return status_from_server
                else:
                    raise HTTPException(status_code=404, detail="Status not found in the response")
            else:
                raise HTTPException(status_code=404, detail="Application not found on the external server")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error calling another server: " + str(e))


@app.post("/api/addAppTracking")
async def add_app_tracking(app_tracking: AppTracking):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Insert the application tracking data into the database
    try:
        cur.execute("""
            INSERT INTO application_tracking (
                application_id, student_name, age, course, competitive_exam, status
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            app_tracking.application_id,
            app_tracking.student_name,
            app_tracking.age,
            app_tracking.course,
            app_tracking.competitive_exam,
            app_tracking.status
        ))

        # Commit the transaction
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting application tracking data: {e}")
    finally:
        cur.close()
        conn.close()