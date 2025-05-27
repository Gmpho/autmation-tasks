#!/usr/bin/env python3
import os
from anthropic import Anthropic

def test_claude_connection():
    """Test the Claude API connection"""
    try:
        # Get API key from environment
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment variables")
        
        # Initialize Anthropic client
        client = Anthropic(api_key=api_key)
        
        # Simple test prompt
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": "Generate a simple test Instagram post about digital marketing."
            }]
        )
        
        print("✅ Claude API connection successful!")
        print("\nSample response:")
        print(message.content)
        
    except Exception as e:
        print("❌ Error connecting to Claude API:")
        print(str(e))

if __name__ == "__main__":
    test_claude_connection()
