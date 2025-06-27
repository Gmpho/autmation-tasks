#!/usr/bin/env python3
"""
Ultra-Secure Mock API Server for Instagram Automation Testing
Simulates all paid services with comprehensive security hardening
Prevents all types of injections: SQL, XSS, Command, Path Traversal
"""

import os
import json
import time
import random
import re
import html
import logging
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify, render_template_string, abort
from flask_cors import CORS
from dotenv import load_dotenv
from mock_ai_generator import MockAIGenerator
from mcp_integration import MCPManager, run_mcp_tool

# Load environment variables
load_dotenv()

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security hardening class
class SecurityValidator:
    """Lightweight security validation for injection prevention"""

    # Dangerous patterns for injection detection
    DANGEROUS_PATTERNS = [
        # SQL injection patterns
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        # XSS patterns
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"vbscript:",
        r"onload\s*=",
        r"onerror\s*=",
        r"onclick\s*=",
        # Command injection patterns
        r"[;&|`$(){}[\]\\]",
        r"\b(cat|ls|pwd|whoami|id|uname|ps|netstat|wget|curl|nc|telnet|ssh)\b",
        # Path traversal patterns
        r"(\.\.\/|\.\.\\)",
        r"(%2e%2e%2f|%2e%2e%5c)",
    ]

    @staticmethod
    def sanitize_input(data):
        """Sanitize input data"""
        if isinstance(data, str):
            # HTML escape
            data = html.escape(data)
            # Remove null bytes
            data = data.replace('\x00', '')
            # Limit length
            if len(data) > 10000:
                data = data[:10000]
        elif isinstance(data, dict):
            return {k: SecurityValidator.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityValidator.sanitize_input(item) for item in data]
        return data

    @staticmethod
    def validate_input(data):
        """Validate input for dangerous patterns"""
        if isinstance(data, str):
            data_lower = data.lower()
            for pattern in SecurityValidator.DANGEROUS_PATTERNS:
                if re.search(pattern, data_lower, re.IGNORECASE):
                    logger.warning(f"Dangerous pattern detected: {pattern}")
                    return False
        elif isinstance(data, dict):
            for key, value in data.items():
                if not SecurityValidator.validate_input(key) or not SecurityValidator.validate_input(value):
                    return False
        elif isinstance(data, list):
            for item in data:
                if not SecurityValidator.validate_input(item):
                    return False
        return True

def security_middleware(f):
    """Security middleware decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Log request
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")

        # Validate JSON data
        if request.is_json:
            try:
                data = request.get_json()
                if data:
                    # Sanitize input
                    data = SecurityValidator.sanitize_input(data)
                    # Validate for dangerous patterns
                    if not SecurityValidator.validate_input(data):
                        logger.warning(f"Malicious input detected from {request.remote_addr}")
                        abort(400, description="Invalid input detected")
                    # Replace request data with sanitized version
                    request._cached_json = (data, data)
            except Exception as e:
                logger.warning(f"Invalid JSON from {request.remote_addr}: {e}")
                abort(400, description="Invalid JSON")

        # Validate query parameters
        for key, value in request.args.items():
            if not SecurityValidator.validate_input(key) or not SecurityValidator.validate_input(value):
                logger.warning(f"Malicious query parameter from {request.remote_addr}")
                abort(400, description="Invalid query parameter")

        # Execute function
        response = f(*args, **kwargs)

        # Add security headers
        if hasattr(response, 'headers'):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Content-Security-Policy'] = "default-src 'self'"
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        return response
    return decorated_function

# Initialize Flask app with security
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Enable CORS with security restrictions
CORS(app,
     origins=['http://localhost:5678', 'http://127.0.0.1:5678'],  # Only n8n
     methods=['GET', 'POST'],
     allow_headers=['Content-Type', 'Authorization'])

# Initialize mock generator and MCP manager
mock_ai = MockAIGenerator()
mcp_manager = MCPManager()

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
@security_middleware
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
@security_middleware
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
@security_middleware
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
@security_middleware
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
@security_middleware
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

# MCP Endpoints
@app.route('/mcp/tools', methods=['GET'])
@security_middleware
def get_mcp_tools():
    """Get available MCP tools"""
    try:
        tools = mcp_manager.get_available_tools()
        return success_response(tools, "MCP tools retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to get MCP tools: {str(e)}")

@app.route('/mcp/<tool_name>', methods=['POST'])
@security_middleware
def call_mcp_tool(tool_name):
    """Call a specific MCP tool"""
    try:
        data = request.get_json()
        if not data:
            return error_response("No parameters provided")

        # Use the synchronous wrapper for MCP calls
        result = run_mcp_tool(tool_name, data)

        # Store in mock database
        result['id'] = len(mock_database["generated_content"]) + 1
        mock_database["generated_content"].append(result)

        return success_response(result, f"MCP tool '{tool_name}' executed successfully")

    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(f"MCP tool execution failed: {str(e)}")

# Specific MCP tool endpoints for easier n8n integration
@app.route('/mcp/filesystem', methods=['POST'])
def mcp_filesystem():
    """File management through MCP"""
    return call_mcp_tool('file_manager')

@app.route('/mcp/research', methods=['POST'])
def mcp_research():
    """Content research through MCP"""
    return call_mcp_tool('content_research')

@app.route('/mcp/images', methods=['POST'])
def mcp_images():
    """Image generation through MCP"""
    return call_mcp_tool('image_generator')

@app.route('/mcp/calendar', methods=['POST'])
def mcp_calendar():
    """Calendar management through MCP"""
    return call_mcp_tool('calendar_manager')

@app.route('/mcp/analytics', methods=['POST'])
def mcp_analytics():
    """Analytics tracking through MCP"""
    return call_mcp_tool('analytics_tracker')

@app.route('/mcp/hashtags', methods=['POST'])
def mcp_hashtags():
    """Hashtag optimization through MCP"""
    return call_mcp_tool('hashtag_optimizer')

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

            <h3>📡 AI Endpoints:</h3>
            <div class="endpoints">
                <span class="endpoint">POST /ai/claude/generate</span>
                <span class="endpoint">POST /ai/openai/generate</span>
                <span class="endpoint">POST /ai/compare</span>
                <span class="endpoint">POST /ai/stories</span>
            </div>

            <h3>🔗 MCP Endpoints:</h3>
            <div class="endpoints">
                <span class="endpoint">GET /mcp/tools</span>
                <span class="endpoint">POST /mcp/filesystem</span>
                <span class="endpoint">POST /mcp/research</span>
                <span class="endpoint">POST /mcp/images</span>
                <span class="endpoint">POST /mcp/calendar</span>
                <span class="endpoint">POST /mcp/analytics</span>
                <span class="endpoint">POST /mcp/hashtags</span>
            </div>

            <h3>📱 Instagram & System:</h3>
            <div class="endpoints">
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

    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(
        host='localhost',
        port=8000,
        debug=debug_mode,
        use_reloader=False  # Prevent double startup in debug mode
    )
