from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    srn: str
    full_name: str
    email: str
    role: str
    resume_link: Optional[str] = None
    skills: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    resume_link: Optional[str]
    skills: Optional[str]

class UserOut(UserBase):
    class Config:
        orm_mode = True

class ProfileData(BaseModel):
    srn:str