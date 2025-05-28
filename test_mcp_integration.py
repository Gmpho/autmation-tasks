#!/usr/bin/env python3
"""
Test script for MCP (Model Context Protocol) integration
Demonstrates all MCP capabilities for Instagram automation
"""

import asyncio
import requests
import json
from datetime import datetime
from mcp_integration import MCPManager

# Mock API base URL
BASE_URL = "http://localhost:8000"

def test_mcp_endpoint(endpoint, data, description):
    """Test an MCP endpoint via the mock API server"""
    print(f"\n{'='*60}")
    print(f"🔗 Testing MCP: {endpoint}")
    print(f"📝 Description: {description}")
    print(f"{'='*60}")
    
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('message', 'OK')}")
            print(f"💰 Cost: {result.get('cost', 'N/A')}")
            
            # Display MCP-specific data
            if 'data' in result and 'data' in result['data']:
                mcp_data = result['data']['data']
                print(f"🔗 MCP Tool: {result['data'].get('tool', 'Unknown')}")
                print(f"📄 Data Preview: {str(mcp_data)[:200]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the mock API server is running!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

async def test_direct_mcp():
    """Test MCP integration directly (without API server)"""
    print(f"\n{'='*60}")
    print("🔗 DIRECT MCP INTEGRATION TEST")
    print(f"{'='*60}")
    
    manager = MCPManager()
    
    # Test each MCP tool directly
    test_cases = [
        {
            "tool": "file_manager",
            "params": {"action": "read", "path": "content_templates/instagram_post.txt"},
            "description": "Read content template file"
        },
        {
            "tool": "content_research",
            "params": {"topic": "Instagram Reels 2024", "platform": "instagram", "limit": 10},
            "description": "Research trending Instagram content"
        },
        {
            "tool": "image_generator",
            "params": {"prompt": "Modern Instagram post about AI automation", "style": "professional", "size": "1080x1080"},
            "description": "Generate Instagram post image"
        },
        {
            "tool": "calendar_manager",
            "params": {"action": "create", "date": "2024-01-15", "time": "09:00", "content": "Morning motivation post"},
            "description": "Schedule content posting"
        },
        {
            "tool": "analytics_tracker",
            "params": {"action": "analyze", "post_id": "instagram_post_123", "metrics": "likes,comments,shares"},
            "description": "Analyze post performance"
        },
        {
            "tool": "hashtag_optimizer",
            "params": {"content": "Amazing Instagram automation tips!", "niche": "socialmedia", "target_audience": "content creators"},
            "description": "Optimize hashtags for maximum reach"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🛠️ Testing {test_case['tool']}: {test_case['description']}")
        try:
            result = await manager.call_tool(test_case['tool'], test_case['params'])
            print(f"✅ Status: {result['status']}")
            print(f"💰 Cost: {result['cost']}")
            print(f"🔗 Tool: {result['tool']}")
            print(f"📊 Mock: {result['mock']}")
            
            # Show specific data based on tool type
            data = result['data']
            if test_case['tool'] == 'file_manager':
                print(f"📁 File: {data.get('path', 'N/A')}")
                print(f"📄 Content: {data.get('content', 'N/A')[:50]}...")
            elif test_case['tool'] == 'content_research':
                print(f"🔍 Topic: {data.get('topic', 'N/A')}")
                print(f"📈 Trending: {data.get('trending_hashtags', [])[:3]}")
            elif test_case['tool'] == 'image_generator':
                print(f"🎨 Style: {data.get('style', 'N/A')}")
                print(f"📐 Size: {data.get('size', 'N/A')}")
                print(f"🖼️ URL: {data.get('image_url', 'N/A')}")
            elif test_case['tool'] == 'calendar_manager':
                print(f"📅 Action: {data.get('action', 'N/A')}")
                if 'event_id' in data:
                    print(f"🆔 Event ID: {data['event_id']}")
            elif test_case['tool'] == 'analytics_tracker':
                metrics = data.get('metrics', {})
                print(f"👍 Likes: {metrics.get('likes', 'N/A')}")
                print(f"💬 Comments: {metrics.get('comments', 'N/A')}")
                print(f"📊 Engagement: {metrics.get('engagement_rate', 'N/A')}")
            elif test_case['tool'] == 'hashtag_optimizer':
                optimized = data.get('optimized_hashtags', {})
                print(f"🎯 High Reach: {optimized.get('high_reach', [])[:3]}")
                print(f"📈 Trending: {optimized.get('trending', [])[:3]}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_mcp_via_api():
    """Test MCP tools via the mock API server"""
    print(f"\n{'='*60}")
    print("🌐 MCP API SERVER INTEGRATION TEST")
    print(f"{'='*60}")
    
    # Test getting available tools
    try:
        response = requests.get(f"{BASE_URL}/mcp/tools")
        if response.status_code == 200:
            tools = response.json()
            print("✅ Available MCP tools retrieved successfully")
            print(f"🛠️ Tools count: {len(tools.get('data', {}))}")
        else:
            print(f"❌ Failed to get MCP tools: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting tools: {e}")
    
    # Test each MCP endpoint
    mcp_tests = [
        {
            "endpoint": "/mcp/filesystem",
            "data": {"action": "list", "path": "/content"},
            "description": "List content files"
        },
        {
            "endpoint": "/mcp/research",
            "data": {"topic": "Instagram Growth Hacks", "platform": "instagram"},
            "description": "Research trending content"
        },
        {
            "endpoint": "/mcp/images",
            "data": {"prompt": "Instagram story about productivity tips", "style": "modern"},
            "description": "Generate story image"
        },
        {
            "endpoint": "/mcp/calendar",
            "data": {"action": "read"},
            "description": "Check posting schedule"
        },
        {
            "endpoint": "/mcp/analytics",
            "data": {"post_id": "test_post_456", "action": "track"},
            "description": "Track post performance"
        },
        {
            "endpoint": "/mcp/hashtags",
            "data": {"content": "Boost your productivity with these amazing tips!", "niche": "productivity"},
            "description": "Optimize hashtags"
        }
    ]
    
    for test in mcp_tests:
        test_mcp_endpoint(test["endpoint"], test["data"], test["description"])

def demo_n8n_mcp_workflow():
    """Demonstrate how to use MCP in n8n workflows"""
    print(f"\n{'='*60}")
    print("📋 N8N MCP WORKFLOW EXAMPLES")
    print(f"{'='*60}")
    
    workflows = [
        {
            "name": "Content Research & Generation",
            "steps": [
                "1. Research trending topics → POST /mcp/research",
                "2. Generate optimized hashtags → POST /mcp/hashtags", 
                "3. Create post content → POST /ai/compare",
                "4. Generate post image → POST /mcp/images",
                "5. Schedule posting → POST /mcp/calendar"
            ]
        },
        {
            "name": "Performance Analytics",
            "steps": [
                "1. Track post metrics → POST /mcp/analytics",
                "2. Analyze performance → POST /mcp/analytics",
                "3. Generate insights report → POST /ai/claude/generate",
                "4. Save report → POST /mcp/filesystem"
            ]
        },
        {
            "name": "Automated Content Pipeline",
            "steps": [
                "1. Check calendar → POST /mcp/calendar",
                "2. Load content template → POST /mcp/filesystem",
                "3. Research current trends → POST /mcp/research",
                "4. Generate personalized content → POST /ai/compare",
                "5. Optimize hashtags → POST /mcp/hashtags",
                "6. Create visuals → POST /mcp/images",
                "7. Post to Instagram → POST /instagram/post",
                "8. Track performance → POST /mcp/analytics"
            ]
        }
    ]
    
    for workflow in workflows:
        print(f"\n🔄 {workflow['name']}:")
        for step in workflow['steps']:
            print(f"   {step}")
    
    print(f"\n💡 MCP Integration Benefits:")
    print("   • File management for content templates")
    print("   • Trend research for relevant content")
    print("   • Image generation for visual posts")
    print("   • Calendar management for scheduling")
    print("   • Advanced analytics and optimization")
    print("   • Hashtag research and optimization")

async def main():
    """Run comprehensive MCP testing"""
    print("🔗 MCP INTEGRATION COMPREHENSIVE TEST")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💰 Total Cost: $0.00 (All Mock)")
    
    # Test direct MCP integration
    await test_direct_mcp()
    
    # Test MCP via API server
    test_mcp_via_api()
    
    # Show n8n workflow examples
    demo_n8n_mcp_workflow()
    
    print(f"\n{'='*60}")
    print("🎉 MCP INTEGRATION TEST COMPLETED")
    print("💰 Total Cost: $0.00 (All Mock)")
    print("🌐 API Dashboard: http://localhost:8000")
    print("🔗 MCP Tools: http://localhost:8000/mcp/tools")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
