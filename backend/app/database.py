"""
Database connection and session management.
Uses Neon Serverless PostgreSQL with connection pooling.
"""
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Import models so SQLModel knows about them when creating tables
from app.models import User, Task  # noqa: F401

# Create database engine with Neon PostgreSQL
# Using pooler URL for better connection management
engine = create_engine(
    settings.DATABASE_URL,
    echo=True if settings.ENVIRONMENT == "development" else False,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10,
)


def create_db_and_tables() -> None:
    """
    Create all database tables defined by SQLModel models.
    Called on application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency for getting database session.
    Automatically closes session after request.

    Usage in routes:
        @app.get("/endpoint")
        def endpoint(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session
