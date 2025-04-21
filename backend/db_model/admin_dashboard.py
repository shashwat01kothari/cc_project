
from typing import List
from pydantic import BaseModel 
class Department(BaseModel):
    course_name: str
    available_seats: int
    total_seats: int

class StudentApplication(BaseModel):
    id: int
    exam: str

class StudentApplicationsResponse(BaseModel):
    applications: List[StudentApplication]

class UpdateStatusRequest(BaseModel):
    status: str

class StudentDataResponse(BaseModel):
    studentName: str
    age: int
    gender: str
    competitiveExam: str
    status : str
