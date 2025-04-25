#port 8003

from fastapi import HTTPException
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/register_student")
async def register(  srn: str,
  full_name: str,
  email: str,
  role: str,
  resume_link: str,
  skills: str,
  password: str):
    try:
        # Send a request to the external server to confirm the seat
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://127.0.0.1:8004/register",json = {
                    "srn": srn,
                    "full_name": full_name,
                    "email": email,
                    "password": password,
                    "role": role,
                    "resume_link": resume_link,
                    "skills": skills
                }
                )
            
            if response.status_code == 200:
                return {"message": "student regiostered with placement service."}
            else:
                raise HTTPException(status_code=404, detail="Seat confirmation failed.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail="Error connecting to external server: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
@app.post("/login_student")
async def login(app_number: str):
    try:
        # Send a request to the external server to confirm the seat
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://127.0.0.1:8004/login",json = {
                    "srn": "22CS1001",
                    "password": "strongpassword123",
                }
                )
            
            if response.status_code == 200:
                return {"message": "student login sucessful"}
            else:
                raise HTTPException(status_code=404, detail="Seat confirmation failed.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail="Error connecting to external server: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    