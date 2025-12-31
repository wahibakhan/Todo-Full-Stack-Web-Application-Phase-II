"""
JWT authentication middleware.
Extracts and verifies JWT tokens from httpOnly cookies.
"""
from typing import Optional
from fastapi import Request, HTTPException, status
from app.core.security import decode_access_token


def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extract JWT token from httpOnly cookie.

    Args:
        request: FastAPI request object

    Returns:
        JWT token string if present, None otherwise
    """
    return request.cookies.get("auth-token")


def verify_jwt_token(request: Request) -> int:
    """
    Verify JWT token and extract user_id.

    Args:
        request: FastAPI request object

    Returns:
        user_id (int) from JWT payload

    Raises:
        HTTPException: 401 if token missing or invalid
    """
    token = get_token_from_cookie(request)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return int(user_id)
