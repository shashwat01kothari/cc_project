from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")


SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{PSQL_PASSWORD}@localhost:5432/integrated_service"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()