"""
Deployment script for Cancer AI Prediction API
Supports different deployment configurations
"""

import os
import uvicorn
from api_server import app

def get_port():
    """Get port from environment variable or default"""
    return int(os.getenv("PORT", 10000))

def get_host():
    """Get host from environment variable or default"""
    return os.getenv("HOST", "0.0.0.0")

if __name__ == "__main__":
    host = get_host()
    port = get_port()
    
    print("🚀 Deploying Cancer AI Prediction API...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"🏥 Health Check: http://{host}:{port}/health")
    
    # Production configuration
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_level="info",
        access_log=True
    )