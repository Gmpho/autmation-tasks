#!/usr/bin/env python3
"""
Simple startup script for the Mock API Server
"""

import subprocess
import sys
import time
import requests

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Flask dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install flask flask-cors")
        return False

def start_server():
    """Start the mock API server"""
    if not check_dependencies():
        return False
    
    print("🚀 Starting Mock API Server...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("🔗 Health check: http://localhost:8000/health")
    print("💰 Cost: $0.00 (FREE)")
    print("-" * 50)
    
    try:
        # Import and run the server
        from mock_api_server import app
        app.run(
            host='localhost',
            port=8000,
            debug=False,  # Disable debug to prevent double startup
            use_reloader=False
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def test_server():
    """Test if server is running"""
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
        # Test mode - check if server is running
        if test_server():
            print("🎉 Server is ready for testing!")
        else:
            print("💡 Start the server with: python start_mock_server.py")
    else:
        # Start mode - launch the server
        start_server()
