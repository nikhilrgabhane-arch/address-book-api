from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# SQLite requires specific connect args for multi-threading context in FastAPI
connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}

try:
    engine = create_engine(
        settings.database_url, 
        connect_args=connect_args,
        echo=settings.debug  # Print SQL queries if in debug mode
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info(f"Database engine created for {settings.database_url}")
except Exception as e:
    logger.critical(f"Failed to intialize database connection: {e}")
    raise

def get_db() -> Generator:
    """
    FastAPI dependency to provide a database session per request.
    Ensures the session is closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
