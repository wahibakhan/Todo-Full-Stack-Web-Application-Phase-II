"""
FastAPI application initialization and configuration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import create_db_and_tables

# Initialize FastAPI application
app = FastAPI(
    title="Todo App API - Phase 2",
    description="Full-stack web application with authentication and persistent storage",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.CORS_ORIGINS == "*" else settings.CORS_ORIGINS.split(","),
    allow_credentials=True,  # Required for cookies (JWT in httpOnly cookie)
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    Run on application startup.
    Creates all database tables if they don't exist.
    """
    create_db_and_tables()


@app.get("/")
def root():
    """Root endpoint - health check."""
    return {
        "message": "Todo App API - Phase 2",
        "status": "running",
        "docs": "/docs",
    }


# Import and register routes
from app.routes import auth, tasks

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
