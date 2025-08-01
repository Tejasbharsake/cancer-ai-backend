"""
Script to start both Python FastAPI backend and Next.js frontend
"""

import subprocess
import sys
import time
import os

def start_python_api():
    """Start the Python FastAPI server"""
    print("🚀 Starting Python FastAPI server...")
    return subprocess.Popen([
        sys.executable, "api_server.py"
    ], cwd=os.getcwd())

def start_nextjs_app():
    """Start the Next.js development server"""
    print("🚀 Starting Next.js frontend...")
    return subprocess.Popen([
        "npm", "run", "dev"
    ], cwd="cancer-ai-web", shell=True)

def main():
    print("=" * 60)
    print("🏥 CANCER AI PREDICTION SYSTEM")
    print("=" * 60)
    
    # Start Python API server
    api_process = start_python_api()
    time.sleep(3)  # Give the API server time to start
    
    # Start Next.js frontend
    frontend_process = start_nextjs_app()
    
    print("\n" + "=" * 60)
    print("✅ SERVERS STARTED SUCCESSFULLY!")
    print("=" * 60)
    print("🔗 Python API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🌐 Frontend: http://localhost:3000")
    print("=" * 60)
    print("Press Ctrl+C to stop both servers")
    
    try:
        # Wait for both processes
        api_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        api_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped successfully!")

if __name__ == "__main__":
    main()