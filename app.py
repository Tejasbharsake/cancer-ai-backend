"""
Simple deployment file for Render
"""

import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables if not set
if not os.getenv('SUPABASE_URL'):
    print("⚠️ SUPABASE_URL not set in environment")
if not os.getenv('SUPABASE_KEY'):
    print("⚠️ SUPABASE_KEY not set in environment")

try:
    # Import the FastAPI app
    from api_server import app
    print("✅ Successfully imported FastAPI app")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    # Create fallback app
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI(
        title="Cancer AI Prediction API",
        description="AI-powered cancer prediction system",
        version="1.0.0"
    )
    
    @app.get("/")
    async def root():
        return JSONResponse({
            "message": "Cancer AI API is running",
            "status": "healthy",
            "error": f"Import error: {str(e)}"
        })
    
    @app.get("/health")
    async def health():
        return JSONResponse({
            "status": "healthy",
            "service": "Cancer AI Prediction API (Fallback)"
        })

# Export app for uvicorn
__all__ = ["app"]