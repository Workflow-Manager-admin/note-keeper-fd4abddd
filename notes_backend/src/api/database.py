import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from .models import Base

# Load .env for DB connection
load_dotenv()

# Get DB URL from environment
DATABASE_URL = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Database URL not configured. Add POSTGRES_URL or DATABASE_URL to .env.")

# PostgreSQL, connect_args for pysqlite only (for completeness)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables if not exist (called at startup)."""
    Base.metadata.create_all(bind=engine)
