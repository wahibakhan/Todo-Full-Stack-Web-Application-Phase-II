"""
Dependency injection functions for FastAPI routes.
"""
from fastapi import Depends, Request
from app.middleware.jwt_auth import verify_jwt_token


def get_current_user(request: Request) -> int:
    """
    Dependency to get current authenticated user ID from JWT.

    This dependency MUST be used in all protected routes.
    It extracts and verifies the JWT token from httpOnly cookie,
    then returns the user_id.

    Usage:
        @router.get("/protected")
        def protected_route(user_id: int = Depends(get_current_user)):
            # user_id is automatically extracted from JWT
            ...

    Args:
        request: FastAPI request object

    Returns:
        user_id (int) from JWT token

    Raises:
        HTTPException 401: If token missing or invalid
    """
    return verify_jwt_token(request)
