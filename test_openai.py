#!/usr/bin/env python3
import os
from openai import OpenAI

def test_openai_connection():
    """Test the OpenAI API connection"""
    try:
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Simple test prompt
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": "Generate a simple test Instagram post about digital marketing."
            }],
            max_tokens=1000,
            temperature=0.7
        )
        
        print("✅ OpenAI API connection successful!")
        print("\nSample response:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print("❌ Error connecting to OpenAI API:")
        print(str(e))

if __name__ == "__main__":
    test_openai_connection()
