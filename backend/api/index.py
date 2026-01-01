"""
Vercel serverless function wrapper for FastAPI app
"""
from app.main import app

# This is required for Vercel to run the FastAPI app
handler = app
