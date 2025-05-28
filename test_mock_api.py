#!/usr/bin/env python3
"""
Test script for Mock API Server
Validates all endpoints and demonstrates usage
"""

import requests
import json
import time
from datetime import datetime

# Mock API base URL
BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, description=""):
    """Test an API endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {method} {endpoint}")
    print(f"📝 Description: {description}")
    print(f"{'='*60}")
    
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message', 'OK')}")
            print(f"💰 Cost: {result.get('cost', 'N/A')}")
            
            # Display relevant data
            if 'data' in result:
                data_preview = str(result['data'])[:200] + "..." if len(str(result['data'])) > 200 else str(result['data'])
                print(f"📄 Data Preview: {data_preview}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the mock API server is running!")
        print("💡 Start it with: python mock_api_server.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🚀 MOCK API SERVER COMPREHENSIVE TEST")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💰 Total Cost: $0.00 (All Mock)")
    
    # Test data for AI generation
    ai_test_data = {
        "topic": "Instagram Growth Strategies",
        "power_words": "proven, explosive, secret, ultimate, guaranteed",
        "emotion": "motivation and urgency",
        "cta": "Save this post for later!",
        "niche": "social media marketing"
    }
    
    # Test data for Instagram posting
    instagram_test_data = {
        "content": "🚀 Boost your Instagram engagement with these proven strategies! Save this post for later.",
        "hashtags": ["#InstagramGrowth", "#SocialMedia", "#DigitalMarketing", "#ContentCreator", "#Engagement"]
    }
    
    # Test data for stories
    stories_test_data = {
        "topic": "AI Tools for Content Creation",
        "style": "professional"
    }
    
    # Run all tests
    test_endpoint("GET", "/health", description="Health check and service status")
    
    test_endpoint("POST", "/ai/claude/generate", ai_test_data, "Generate content with mock Claude AI")
    
    test_endpoint("POST", "/ai/openai/generate", ai_test_data, "Generate content with mock OpenAI")
    
    test_endpoint("POST", "/ai/compare", ai_test_data, "Compare both AI providers")
    
    test_endpoint("POST", "/ai/stories", stories_test_data, "Generate Instagram Stories")
    
    test_endpoint("POST", "/instagram/post", instagram_test_data, "Mock Instagram posting")
    
    test_endpoint("GET", "/analytics", description="Get analytics and usage statistics")
    
    print(f"\n{'='*60}")
    print("🎉 COMPREHENSIVE TEST COMPLETED")
    print("💰 Total Cost: $0.00 (All Mock)")
    print("🌐 Dashboard: http://localhost:8000")
    print(f"{'='*60}")

def demo_n8n_integration():
    """Demonstrate how to use these endpoints in n8n"""
    print(f"\n{'='*60}")
    print("📋 N8N INTEGRATION EXAMPLES")
    print(f"{'='*60}")
    
    examples = [
        {
            "workflow": "Content Generation",
            "method": "POST",
            "url": f"{BASE_URL}/ai/compare",
            "description": "Generate content with both AI providers and compare results"
        },
        {
            "workflow": "Instagram Posting",
            "method": "POST", 
            "url": f"{BASE_URL}/instagram/post",
            "description": "Post generated content to Instagram (mock)"
        },
        {
            "workflow": "Stories Creation",
            "method": "POST",
            "url": f"{BASE_URL}/ai/stories",
            "description": "Generate Instagram Stories content"
        },
        {
            "workflow": "Analytics Monitoring",
            "method": "GET",
            "url": f"{BASE_URL}/analytics",
            "description": "Monitor automation performance and usage"
        }
    ]
    
    for example in examples:
        print(f"\n🔧 {example['workflow']}:")
        print(f"   Method: {example['method']}")
        print(f"   URL: {example['url']}")
        print(f"   Use: {example['description']}")
    
    print(f"\n💡 In n8n:")
    print("1. Use 'HTTP Request' nodes")
    print("2. Set Method and URL from examples above")
    print("3. Add JSON data in the body")
    print("4. Process the response in subsequent nodes")

if __name__ == "__main__":
    print("🧪 MOCK API TESTING SUITE")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Mock API Server is running!")
            
            # Run comprehensive tests
            run_comprehensive_test()
            
            # Show n8n integration examples
            demo_n8n_integration()
            
        else:
            print("❌ Mock API Server responded with error")
            
    except requests.exceptions.ConnectionError:
        print("❌ Mock API Server is not running!")
        print("\n🚀 To start the server:")
        print("1. Install dependencies: pip install flask flask-cors")
        print("2. Run server: python mock_api_server.py")
        print("3. Run this test again: python test_mock_api.py")
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💰 Total testing cost: $0.00")
