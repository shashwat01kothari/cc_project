#port 8004

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User & Profile Microservice")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.role not in {"student", "faculty", "admin", "recruiter"}:
        raise HTTPException(status_code=400, detail="Invalid role")
    if crud.get_user_by_srn(db, user.srn):
        raise HTTPException(status_code=400, detail="SRN already registered")
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.UserOut)
def login(srn: str, password: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, srn, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.get("/profile/{srn}", response_model=schemas.UserOut)
def get_profile(srn: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_srn(db, srn)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/profile/{srn}", response_model=schemas.UserOut)
def update_profile(srn: str, update_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, srn, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

