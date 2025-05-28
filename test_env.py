#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_environment():
    """Test if environment variables are loaded correctly"""
    print("🔍 Checking environment variables...")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        print("💡 Create a .env file by copying .env.example:")
        print("   cp .env.example .env")
        return
    
    # Check API keys
    claude_key = os.getenv('CLAUDE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    print(f"\n📋 Environment Variables Status:")
    print(f"CLAUDE_API_KEY: {'✅ Set' if claude_key else '❌ Not set'}")
    print(f"OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
    
    if claude_key:
        print(f"Claude key preview: {claude_key[:10]}...{claude_key[-4:]}")
    
    if openai_key:
        print(f"OpenAI key preview: {openai_key[:10]}...{openai_key[-4:]}")
    
    # Check other variables
    other_vars = [
        'N8N_BASIC_AUTH_USER',
        'N8N_BASIC_AUTH_PASSWORD',
        'N8N_EDITOR_BASE_URL',
        'WEBHOOK_URL',
        'INSTAGRAM_ACCESS_TOKEN'
    ]
    
    print(f"\n🔧 Other Variables:")
    for var in other_vars:
        value = os.getenv(var)
        print(f"{var}: {'✅ Set' if value else '❌ Not set'}")

if __name__ == "__main__":
    test_environment()
