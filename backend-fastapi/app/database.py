from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

# ==========================================
# 1. POSTGRESQL (Core ERP Data)
# ==========================================
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:YOUR_PASSWORD@localhost:5432/procureiq_db" 
)

# PostgreSQL Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# 2. MONGODB (NoSQL Bonus: AI Logs)
# ==========================================
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Motor Async Client for MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
mongo_db = client.procureiq_ai
ai_logs_collection = mongo_db.ai_logs