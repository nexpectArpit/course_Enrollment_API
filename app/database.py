"""
Database configuration and session management.

This module handles:
- Database connection setup using SQLAlchemy
- Session management for database operations
- Base class for ORM models
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This includes DATABASE_URL with PostgreSQL connection details
load_dotenv()

# Get database URL from environment variables
# Format: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
# This manages the connection pool to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create SessionLocal class for database sessions
# autocommit=False: Transactions must be explicitly committed
# autoflush=False: Changes are not automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
# All model classes (Student, Course, etc.) inherit from this
Base = declarative_base()

def get_db():
    """
    Dependency function that provides database session to route handlers.
    
    This function is used with FastAPI's Depends() to inject a database session
    into route handlers. It ensures the session is properly closed after use.
    
    Usage in routes:
        def my_route(db: Session = Depends(get_db)):
            # Use db here
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session, even if an error occurs
        db.close()
