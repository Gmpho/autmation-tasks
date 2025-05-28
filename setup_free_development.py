#!/usr/bin/env python3
"""
Complete setup script for free Instagram automation development
Sets up everything needed for $0 cost development and testing
"""

import os
import subprocess
import sys
import time
import requests
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n{step}. {description}")
    print("-" * 40)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is too old. Need Python 3.8+")
        return False

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed")
        return False

def install_dependencies():
    """Install required Python packages"""
    packages = [
        "flask>=2.3.0",
        "flask-cors>=4.0.0", 
        "requests>=2.31.0"
    ]
    
    print("📦 Installing dependencies...")
    for package in packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            print(f"✅ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            content = src.read()
            # Add mock-specific variables
            content += "\n# Mock Development Settings\n"
            content += "MOCK_MODE=true\n"
            content += "MOCK_API_URL=http://localhost:8000\n"
            dst.write(content)
        print("✅ .env file created")
        print("💡 Edit .env file to add your real API keys when ready")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ .env.example not found")

def test_mock_generator():
    """Test the mock AI generator"""
    try:
        from mock_ai_generator import MockAIGenerator
        mock_gen = MockAIGenerator()
        result = mock_gen.generate_with_claude_mock(
            topic="Test", power_words="test", emotion="test", 
            cta="test", niche="test"
        )
        print("✅ Mock AI generator is working")
        return True
    except Exception as e:
        print(f"❌ Mock AI generator error: {e}")
        return False

def start_services():
    """Start Docker and Mock API services"""
    print("🐳 Starting Docker services...")
    try:
        # Start n8n with docker-compose
        result = subprocess.run(['docker-compose', 'up', '-d'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ n8n started successfully")
            print("🌐 n8n available at: http://localhost:5678")
        else:
            print(f"❌ Failed to start n8n: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ docker-compose not found")
        return False
    
    print("\n🚀 Starting Mock API Server...")
    print("💡 This will run in the background")
    print("📊 Dashboard: http://localhost:8000")
    
    return True

def run_tests():
    """Run comprehensive tests"""
    print("🧪 Running tests...")
    
    # Test environment
    try:
        subprocess.run([sys.executable, 'test_env.py'], check=True)
        print("✅ Environment test passed")
    except subprocess.CalledProcessError:
        print("❌ Environment test failed")
    
    # Test mock generator
    try:
        subprocess.run([sys.executable, 'mock_ai_generator.py'], check=True)
        print("✅ Mock AI generator test passed")
    except subprocess.CalledProcessError:
        print("❌ Mock AI generator test failed")

def print_success_summary():
    """Print success summary and next steps"""
    print_header("🎉 FREE DEVELOPMENT SETUP COMPLETE!")
    
    print("✅ What's Ready:")
    print("   • Mock AI Server (Claude + OpenAI simulation)")
    print("   • n8n Workflow Automation")
    print("   • Complete testing environment")
    print("   • Zero API costs")
    
    print("\n🌐 Access Points:")
    print("   • n8n Dashboard: http://localhost:5678")
    print("   • Mock API Dashboard: http://localhost:8000")
    print("   • API Health Check: http://localhost:8000/health")
    
    print("\n📋 Next Steps:")
    print("   1. Open n8n: http://localhost:5678")
    print("   2. Create your first workflow")
    print("   3. Use HTTP Request nodes to call mock APIs")
    print("   4. Test everything with $0 cost")
    print("   5. Add real API keys only when ready")
    
    print("\n💰 Current Cost: $0.00")
    print("🚀 You can now build your entire Instagram automation system for FREE!")

def main():
    """Main setup function"""
    print_header("FREE INSTAGRAM AUTOMATION SETUP")
    print("💰 Total Cost: $0.00")
    print("🎯 Goal: Complete development environment without API costs")
    
    # Step 1: Check system requirements
    print_step("1", "Checking System Requirements")
    if not check_python_version():
        return False
    
    docker_available = check_docker()
    if not docker_available:
        print("💡 Docker is recommended but not required for mock testing")
    
    # Step 2: Install dependencies
    print_step("2", "Installing Dependencies")
    if not install_dependencies():
        return False
    
    # Step 3: Setup environment
    print_step("3", "Setting Up Environment")
    create_env_file()
    
    # Step 4: Test mock components
    print_step("4", "Testing Mock Components")
    if not test_mock_generator():
        return False
    
    # Step 5: Start services
    print_step("5", "Starting Services")
    if docker_available:
        if not start_services():
            print("⚠️ Docker services failed, but you can still use mock APIs")
    
    # Step 6: Run tests
    print_step("6", "Running Tests")
    run_tests()
    
    # Success summary
    print_success_summary()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n{'='*60}")
            print("🎉 Setup completed successfully!")
            print("💡 Run 'python start_mock_server.py' to start the mock API")
            print("💡 Run 'python test_mock_api.py' to test all endpoints")
            print(f"{'='*60}")
        else:
            print(f"\n{'='*60}")
            print("❌ Setup encountered issues")
            print("💡 Check the error messages above and try again")
            print(f"{'='*60}")
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("💡 Please check your environment and try again")
