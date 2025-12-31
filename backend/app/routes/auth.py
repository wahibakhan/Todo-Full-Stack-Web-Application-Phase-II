"""
Authentication routes: signup, login, logout.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, AuthResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(
    signup_data: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Create a new user account.

    - Validates email format (Pydantic)
    - Validates password length (min 8 characters)
    - Checks if email already exists (409 Conflict)
    - Hashes password with bcrypt
    - Creates user in database
    - Returns user info (does NOT issue JWT - user must login)
    """
    # Check if email already exists
    statement = select(User).where(User.email == signup_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(signup_data.password)

    # Create new user
    new_user = User(
        email=signup_data.email,
        hashed_password=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return AuthResponse(
        user_id=new_user.id,
        email=new_user.email,
        message="Account created successfully"
    )


@router.post("/login", response_model=AuthResponse)
def login(
    login_data: LoginRequest,
    response: Response,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and issue JWT token.

    - Validates credentials
    - Issues JWT token in httpOnly cookie
    - Returns user info

    Security:
    - Generic error message ("Invalid credentials") prevents user enumeration
    - JWT stored in httpOnly cookie (XSS protection)
    """
    # Find user by email
    statement = select(User).where(User.email == login_data.email)
    user = session.exec(statement).first()

    # Verify password
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"  # Generic message for security
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # Set token in httpOnly cookie
    response.set_cookie(
        key="auth-token",
        value=access_token,
        httponly=True,  # XSS protection
        secure=False,  # Set to True in production (HTTPS only)
        samesite="lax",  # CSRF protection
        max_age=86400  # 24 hours
    )

    return AuthResponse(
        user_id=user.id,
        email=user.email,
        message="Logged in successfully"
    )


@router.post("/logout")
def logout(
    response: Response,
    user_id: int = Depends(get_current_user)
):
    """
    Log out current user by clearing JWT cookie.

    Requires authentication (JWT token).
    """
    # Clear the auth cookie
    response.set_cookie(
        key="auth-token",
        value="",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=0  # Expire immediately
    )

    return {"message": "Logged out successfully"}
