from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "users"

    srn = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    resume_link = Column(String, nullable=True)
    skills = Column(String, nullable=True)