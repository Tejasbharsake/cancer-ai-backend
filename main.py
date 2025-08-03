"""
Main entry point for the Cancer AI Prediction API
This file is used for deployment with uvicorn
"""

import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from api_server import app
    print("✅ Successfully imported app from api_server")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Fallback: create a simple app
    from fastapi import FastAPI
    app = FastAPI(title="Cancer AI API - Fallback")
    
    @app.get("/")
    async def root():
        return {"message": "Cancer AI API is running (fallback mode)", "error": str(e)}

# This allows uvicorn to find the app
# Usage: uvicorn main:app --host=0.0.0.0 --port=10000

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    print("🚀 Starting Cancer AI Prediction API...")
    print(f"📍 Server will be available at: http://0.0.0.0:{port}")
    print(f"📚 API docs will be available at: http://0.0.0.0:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)