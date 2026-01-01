"""
Vercel serverless function wrapper for FastAPI app
"""
import sys
import os

# Add backend directory to Python path so we can import from app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app

# This is required for Vercel to run the FastAPI app
handler = app
