import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from typing import Generator
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Configure local session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Safe database session generator with error printing:
    1. Prints errors to console
    2. Always closes the session
    3. Handles commits/rollbacks automatically
    
    Usage:
        with get_db() as db:
            # Your database operations
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {str(e)}")
        raise
    finally:
        db.close()