#!/usr/bin/env python3
"""
Simple startup script for the Mock API Server (FastAPI + Uvicorn)
"""

import subprocess
import sys
import requests


def check_dependencies():
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI + Uvicorn dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install fastapi uvicorn")
        return False


def start_server():
    if not check_dependencies():
        return False

    print("🚀 Starting Mock API Server (FastAPI)...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("🔗 Health check: http://localhost:8000/health")
    print("📖 API docs: http://localhost:8000/docs")
    print("-" * 50)

    try:
        import uvicorn
        uvicorn.run("mock_api_server:app", host="localhost", port=8000, reload=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False


def test_server():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Mock API Server is running successfully!")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False


if __name__ == "__main__":
    print("🧪 MOCK API SERVER STARTUP")
    print("=" * 40)

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        if test_server():
            print("🎉 Server is ready for testing!")
        else:
            print("💡 Start the server with: python start_mock_server.py")
    else:
        start_server()
