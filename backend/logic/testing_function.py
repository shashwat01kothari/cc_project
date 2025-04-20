from fastapi import Depends, HTTPException
from psycopg2.extensions import connection
from cc_proj.backend.db_connection.conection import get_db

from cc_proj.backend.db_model.admin_dashboard import UpdateStatusRequest

def verify_student_documents(application_id: int, request: str ,db:connection):

    # Connect to the database
    cur=db.cursor()

    # Update the student's status in the database
    try:
        cur.execute("""
            UPDATE application_data
            SET status = "pending"
            WHERE id = %s AND status = 'unverified';
        """, (request.status, application_id))
        
        

        # Check if the update was successful
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student application not found or already verified")
        db.commit()
        cur.close()
        # Return success response
        return {"message": "Student application status updated successfully."}
    
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
# If running as a script (not via FastAPI route)
if __name__ == "__main__":
    from cc_proj.backend.db_connection.conection import get_db

    # Since get_db is a generator, use next() to get the connection
    db_gen = get_db()
    db = next(db_gen)
    try:
        verify_student_documents(application_id=1,request="verified",db=db)
    finally:
        db_gen.close()