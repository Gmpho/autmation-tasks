#!/usr/bin/env python3
"""
Professional Mock API Server for Instagram Automation Testing
Simulates all paid services (Claude AI, OpenAI, Instagram API) for free local development
"""

import os
import json
import time
import random
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
from mock_ai_generator import MockAIGenerator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for n8n integration

# Initialize mock generator
mock_ai = MockAIGenerator()

# Mock database for storing generated content
mock_database = {
    "generated_content": [],
    "instagram_posts": [],
    "analytics": {
        "total_requests": 0,
        "ai_generations": 0,
        "instagram_posts": 0
    }
}

# API Response helpers
def success_response(data, message="Success"):
    """Standard success response format"""
    return jsonify({
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat(),
        "cost": "$0.00 (Mock)"
    })

def error_response(message, code=400):
    """Standard error response format"""
    return jsonify({
        "status": "error",
        "message": message,
        "timestamp": datetime.now().isoformat()
    }), code

# Middleware for request logging
@app.before_request
def log_request():
    """Log all incoming requests"""
    mock_database["analytics"]["total_requests"] += 1
    print(f"📥 {request.method} {request.path} - Request #{mock_database['analytics']['total_requests']}")

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response({
        "service": "Mock API Server",
        "status": "healthy",
        "uptime": "Running",
        "endpoints": [
            "/ai/claude/generate",
            "/ai/openai/generate", 
            "/ai/compare",
            "/instagram/post",
            "/instagram/stories",
            "/analytics"
        ]
    })

# Claude AI Mock Endpoint
@app.route('/ai/claude/generate', methods=['POST'])
def claude_generate():
    """Mock Claude AI content generation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['topic', 'power_words', 'emotion', 'cta', 'niche']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}")
        
        # Simulate API delay
        time.sleep(random.uniform(0.5, 2.0))
        
        # Generate mock content
        result = mock_ai.generate_with_claude_mock(
            topic=data['topic'],
            power_words=data['power_words'],
            emotion=data['emotion'],
            cta=data['cta'],
            niche=data['niche']
        )
        
        # Store in mock database
        result['id'] = len(mock_database["generated_content"]) + 1
        result['timestamp'] = datetime.now().isoformat()
        mock_database["generated_content"].append(result)
        mock_database["analytics"]["ai_generations"] += 1
        
        return success_response(result, "Claude content generated successfully")
        
    except Exception as e:
        return error_response(f"Claude generation failed: {str(e)}")

# OpenAI Mock Endpoint
@app.route('/ai/openai/generate', methods=['POST'])
def openai_generate():
    """Mock OpenAI content generation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['topic', 'power_words', 'emotion', 'cta', 'niche']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}")
        
        # Simulate API delay
        time.sleep(random.uniform(0.5, 2.0))
        
        # Generate mock content
        result = mock_ai.generate_with_openai_mock(
            topic=data['topic'],
            power_words=data['power_words'],
            emotion=data['emotion'],
            cta=data['cta'],
            niche=data['niche']
        )
        
        # Store in mock database
        result['id'] = len(mock_database["generated_content"]) + 1
        result['timestamp'] = datetime.now().isoformat()
        mock_database["generated_content"].append(result)
        mock_database["analytics"]["ai_generations"] += 1
        
        return success_response(result, "OpenAI content generated successfully")
        
    except Exception as e:
        return error_response(f"OpenAI generation failed: {str(e)}")

# AI Comparison Endpoint
@app.route('/ai/compare', methods=['POST'])
def ai_compare():
    """Compare both AI providers"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['topic', 'power_words', 'emotion', 'cta', 'niche']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}")
        
        # Simulate API delay for both providers
        time.sleep(random.uniform(1.0, 3.0))
        
        # Generate comparison
        result = mock_ai.compare_outputs_mock(
            topic=data['topic'],
            power_words=data['power_words'],
            emotion=data['emotion'],
            cta=data['cta'],
            niche=data['niche']
        )
        
        # Add metadata
        comparison_result = {
            "comparison_id": len(mock_database["generated_content"]) + 1,
            "timestamp": datetime.now().isoformat(),
            "providers": result,
            "recommendation": "Both providers generated quality content. Choose based on your preference.",
            "total_cost": "$0.00 (Mock)"
        }
        
        mock_database["generated_content"].append(comparison_result)
        mock_database["analytics"]["ai_generations"] += 2
        
        return success_response(comparison_result, "AI comparison completed successfully")
        
    except Exception as e:
        return error_response(f"AI comparison failed: {str(e)}")

# Instagram Stories Mock Endpoint
@app.route('/ai/stories', methods=['POST'])
def generate_stories():
    """Mock Instagram Stories generation"""
    try:
        data = request.get_json()
        topic = data.get('topic', 'General Topic')
        style = data.get('style', 'casual')
        
        # Simulate API delay
        time.sleep(random.uniform(0.5, 1.5))
        
        result = mock_ai.generate_stories_mock(topic, style)
        result['id'] = len(mock_database["generated_content"]) + 1
        result['timestamp'] = datetime.now().isoformat()
        
        mock_database["generated_content"].append(result)
        
        return success_response(result, "Instagram Stories generated successfully")
        
    except Exception as e:
        return error_response(f"Stories generation failed: {str(e)}")

# Mock Instagram Post Endpoint
@app.route('/instagram/post', methods=['POST'])
def instagram_post():
    """Mock Instagram posting"""
    try:
        data = request.get_json()
        
        required_fields = ['content', 'hashtags']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}")
        
        # Simulate posting delay
        time.sleep(random.uniform(1.0, 3.0))
        
        # Mock successful post
        post_result = {
            "post_id": f"mock_post_{random.randint(1000, 9999)}",
            "status": "published",
            "content": data['content'],
            "hashtags": data['hashtags'],
            "timestamp": datetime.now().isoformat(),
            "engagement": {
                "likes": random.randint(10, 100),
                "comments": random.randint(1, 20),
                "shares": random.randint(0, 10)
            },
            "reach": random.randint(100, 1000),
            "url": f"https://instagram.com/p/mock_post_{random.randint(1000, 9999)}"
        }
        
        mock_database["instagram_posts"].append(post_result)
        mock_database["analytics"]["instagram_posts"] += 1
        
        return success_response(post_result, "Instagram post published successfully")
        
    except Exception as e:
        return error_response(f"Instagram posting failed: {str(e)}")

# Analytics Endpoint
@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get mock analytics data"""
    analytics = {
        **mock_database["analytics"],
        "recent_content": mock_database["generated_content"][-5:],
        "recent_posts": mock_database["instagram_posts"][-5:],
        "server_uptime": "Running",
        "total_cost": "$0.00 (All Mock)"
    }
    
    return success_response(analytics, "Analytics retrieved successfully")

# Dashboard Endpoint
@app.route('/', methods=['GET'])
def dashboard():
    """Simple dashboard for monitoring"""
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mock API Server Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            .stats { display: flex; gap: 20px; margin: 20px 0; }
            .stat-box { background: #3498db; color: white; padding: 20px; border-radius: 5px; flex: 1; text-align: center; }
            .endpoints { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #2ecc71; color: white; padding: 5px 10px; margin: 5px; border-radius: 3px; display: inline-block; }
            .status { color: #27ae60; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="header">🚀 Mock API Server Dashboard</h1>
            <p class="status">Status: ✅ Running (FREE)</p>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>{{ analytics.total_requests }}</h3>
                    <p>Total Requests</p>
                </div>
                <div class="stat-box">
                    <h3>{{ analytics.ai_generations }}</h3>
                    <p>AI Generations</p>
                </div>
                <div class="stat-box">
                    <h3>{{ analytics.instagram_posts }}</h3>
                    <p>Instagram Posts</p>
                </div>
            </div>
            
            <h3>📡 Available Endpoints:</h3>
            <div class="endpoints">
                <span class="endpoint">POST /ai/claude/generate</span>
                <span class="endpoint">POST /ai/openai/generate</span>
                <span class="endpoint">POST /ai/compare</span>
                <span class="endpoint">POST /ai/stories</span>
                <span class="endpoint">POST /instagram/post</span>
                <span class="endpoint">GET /analytics</span>
                <span class="endpoint">GET /health</span>
            </div>
            
            <h3>💡 Usage:</h3>
            <p>Use these endpoints in your n8n workflows to test automation without API costs!</p>
            <p><strong>Base URL:</strong> http://localhost:8000</p>
            <p><strong>Total Cost:</strong> $0.00 (All Mock)</p>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(dashboard_html, analytics=mock_database["analytics"])

if __name__ == '__main__':
    print("🚀 Starting Mock API Server...")
    print("📊 Dashboard: http://localhost:8000")
    print("🔗 Health Check: http://localhost:8000/health")
    print("💰 Cost: $0.00 (FREE)")
    print("-" * 50)
    
    app.run(
        host='localhost',
        port=8000,
        debug=True,
        use_reloader=False  # Prevent double startup in debug mode
    )
