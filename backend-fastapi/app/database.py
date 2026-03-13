import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# --- SQLite Setup (No installation required!) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./po_database.db"

# check_same_thread is needed for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- MongoDB Setup (For AI Logs) ---
# If no URL is provided, it will just use a local dummy connection 
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client["po_ai_logs"]
ai_logs_collection = mongo_db["prompts_and_responses"]