from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile, Depends
from typing import List, Optional
from fastapi.responses import JSONResponse
from psycopg2.extensions import connection

from cc_proj.backend.db_connection.conection import get_db

from cc_proj.backend.db_model.admin_dashboard import Department, StudentApplicationsResponse, StudentDataResponse, UpdateStatusRequest


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#student portal
@app.post("/api/studentPortal")
async def student_portal(
    studentName: str = Form(...),
    age: str = Form(...),
    gender: str = Form(...),
    studentPhoto: UploadFile = File(...),
    marks10: UploadFile = File(...),
    marks12: UploadFile = File(...),
    competitiveExam: str = Form(...),
    examPdf: Optional[UploadFile] = File(None),
    course: str = Form(...),  # New course field
    db: connection = Depends(get_db)  # Injected db connection
):
    # Read file contents
    studentPhoto_content = await studentPhoto.read()
    marks10_content = await marks10.read()
    marks12_content = await marks12.read()
    examPdf_content = await (examPdf.read() if examPdf else None)
    
    try:
        # Insert data using the provided db connection with RETURNING to get the inserted ID
        cur = db.cursor()
        cur.execute("""
            INSERT INTO application_data(
                student_name, age, gender, student_photo,
                marksheet_10th, marksheet_12th,
                competitive_exam, exam_marksheet, course_applied
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;  -- Get the ID of the inserted row
        """, (
            studentName,
            int(age),
            gender,
            studentPhoto_content,
            marks10_content,
            marks12_content,
            competitiveExam,
            examPdf_content,
            course  # Store course selection
        ))
        
        # Fetch the inserted application ID
        application_id = cur.fetchone()[0]

        # Commit the transaction
        db.commit()

        cur.close()

        return {"message": "Application submitted successfully", "application_id": application_id}
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(status_code=500, content={"message": "Error in submission"})


@app.get("/api/seatInfo", response_model=List[Department])
async def get_seat_information( db: connection=Depends(get_db)):
    try:
        cur = db.cursor()
        cur.execute("SELECT course_name, available_seats, total_seats FROM seat_information;")

            # Fetch all the results
        rows = cur.fetchall()

        # Return the fetched data
        seat_info = []
        for row in rows:
            seat_info.append({
                "course_name": row[0],
                "available_seats": row[1],
                "total_seats": row[2]
            })
        cur.close()
        print(seat_info , "done ")
        return seat_info
    # Close the cursor and connection
    except Exception as e:
        print(f"Error: {e}")


@app.get("/api/studentApplications", response_model=StudentApplicationsResponse)
async def get_student_applications(db:connection=Depends(get_db)):
    try:
        cur = db.cursor()
        cur.execute("SELECT id, competitive_exam FROM application_data WHERE status = 'applied' LIMIT 5;")

        # Fetch all the results
        rows = cur.fetchall()

        # Prepare the response data
        applications = []
        for row in rows:
            applications.append({
                "id": row[0],
                "exam": row[1]
            })

        # Close the cursor and connection
        cur.close()

        print(applications, "done")

        return {"applications": applications}

    except Exception as e:
        print(f"Error: {e}")
        return {"applications": []}
    
@app.put("/api/studentApplications/verify/{application_id}")
async def verify_student_documents(application_id: int,db:connection=Depends(get_db)):

    # Connect to the database
    cur=db.cursor()

    # Update the student's status in the database
    try:
        cur.execute("""
            UPDATE application_data SET status = 'approved' WHERE id = %s;
        """, (application_id ,))
        
        db.commit()
        

        # Check if the update was successful
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student application not found or already verified")
        db.commit()
        cur.close()
        # Return success response
        return {"message": "Student application status updated successfully."}
    
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@app.get("/api/getData", response_model=Optional[StudentDataResponse])
async def get_student_data(appNumber: str = Query(...), db:connection = Depends(get_db)):
    try:
        cur = db.cursor()
        cur.execute("""
            SELECT student_name, age, gender, competitive_exam , status
            FROM application_data 
            WHERE id = %s
        """, (appNumber,))

        row = cur.fetchone()
        cur.close()

        if not row:
            raise HTTPException(status_code=404, detail="Application not found")

        return {
            "studentName": row[0],
            "age": row[1],
            "gender": row[2],
            "competitiveExam": row[3],
            "status" : row[4]
        }

    except Exception as e:
        print(f"Error fetching application data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    



@app.post("/api/confirmSeat", response_model=StudentDataResponse)
async def confirm_seat(appNumber: str = Query(...), db: connection = Depends(get_db)):
    try:
        # Step 1: Fetch student data
        cur = db.cursor()
        cur.execute("""
            SELECT student_name, age, gender, competitive_exam, status , course_applied
            FROM application_data 
            WHERE id = %s
        """, (appNumber,))

        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Application not found")

        student_name, age, gender, competitive_exam, status, course_applied = row

        # Step 2: Check if document verification is approved
        if status.lower() != "approved":
            raise HTTPException(status_code=400, detail="Document verification is not approved")

        # Step 3: Reduce available seats for the course in seat_information table
        cur.execute("""
            UPDATE seat_information 
            SET available_seats = available_seats - 1
            WHERE course_name = %s
        """, (course_applied,))
        db.commit()

        # Step 4: Insert student data into admissions_2025 table
        cur.execute("""
            INSERT INTO admissions_2025 (application_id, student_name, age, gender, competitive_exam, course_applied)
            SELECT id, student_name, age, gender, competitive_exam, course_applied
            FROM application_data
            WHERE id = %s
        """, (appNumber,))
        db.commit()

        cur.close()

        # Return the updated student data with seatConfirmed set to True
        return {
            "studentName": student_name,
            "age": age,
            "gender": gender,
            "competitiveExam": competitive_exam,
            "status": status,
            "seatConfirmed": True
        }

    except Exception as e:
        print(f"Error confirming seat: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
