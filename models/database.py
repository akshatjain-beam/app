# models.database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database URL for SQLite
DATABASE_URL = "sqlite:///products.db"

# Create an engine that stores data in the local directory's products.db file.
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

def get_local_session() -> Session:
    """
    Create and return a new SQLAlchemy session.
    
    This function creates a new database session and returns it.
    It is typically used in a context where a new session is needed.
    
    Returns:
        db (Session): A new SQLAlchemy database session.
    """
    db = SessionLocal()
    return db

# Create a base class for our classes definitions
Base = declarative_base()
