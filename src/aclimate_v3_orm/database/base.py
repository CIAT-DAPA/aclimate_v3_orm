from sqlalchemy.orm import declarative_base
from . import engine

Base = declarative_base()


def create_tables():
    """
    Creates all tables defined in SQLAlchemy models.
    
    Raises:
        Exception: If table creation fails, the original exception is re-raised.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise  # Re-raise the exception for external handling