"""
User model for authentication.
Managed by Better Auth JWT system.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    User model representing a registered user account.

    Fields:
        id: Auto-incrementing primary key
        email: Unique email address (used for login)
        hashed_password: Bcrypt hashed password (never store plaintext)
        created_at: Account creation timestamp
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2025-12-29T10:00:00Z"
            }
        }
