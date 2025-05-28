#!/bin/bash

# Instagram Automation - Cloud Startup Script
# Quick deployment to cloud with ngrok free domain

set -e

echo "🚀 Instagram Automation - Cloud Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env.cloud exists
if [ ! -f ".env.cloud" ]; then
    echo -e "${YELLOW}⚠️ .env.cloud not found${NC}"
    echo "📋 Creating from template..."
    cp .env.cloud.example .env.cloud
    echo -e "${RED}❌ Please configure .env.cloud with your settings${NC}"
    echo "💡 Required: NGROK_AUTHTOKEN, N8N_BASIC_AUTH_USER, N8N_BASIC_AUTH_PASSWORD"
    echo "🔗 Get free ngrok token: https://dashboard.ngrok.com/get-started/your-authtoken"
    exit 1
fi

# Load environment
source .env.cloud

# Check required variables
if [ -z "$NGROK_AUTHTOKEN" ] || [ -z "$N8N_BASIC_AUTH_USER" ] || [ -z "$N8N_BASIC_AUTH_PASSWORD" ]; then
    echo -e "${RED}❌ Missing required environment variables${NC}"
    echo "💡 Configure NGROK_AUTHTOKEN, N8N_BASIC_AUTH_USER, N8N_BASIC_AUTH_PASSWORD in .env.cloud"
    exit 1
fi

echo -e "${GREEN}✅ Environment configuration loaded${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found${NC}"
    echo "💡 Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found${NC}"
    echo "💡 Install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose found${NC}"

# Stop any existing services
echo "🛑 Stopping existing services..."
docker-compose -f docker-compose.cloud.yml down --remove-orphans 2>/dev/null || true

# Build images
echo "🏗️ Building Docker images..."
docker build -f Dockerfile.mock-api -t instagram-automation-api:latest .

# Start services
echo "🚀 Starting cloud services..."
docker-compose -f docker-compose.cloud.yml --env-file .env.cloud up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Check Mock API
if curl -f http://localhost:8000/health &>/dev/null; then
    echo -e "${GREEN}✅ Mock API is healthy${NC}"
else
    echo -e "${YELLOW}⚠️ Mock API starting...${NC}"
fi

# Check n8n
if curl -f http://localhost:5678/healthz &>/dev/null; then
    echo -e "${GREEN}✅ n8n is healthy${NC}"
else
    echo -e "${YELLOW}⚠️ n8n starting...${NC}"
fi

# Get ngrok URLs
echo "🌐 Getting external URLs..."
sleep 10

if curl -f http://localhost:4040/api/tunnels &>/dev/null; then
    echo -e "${GREEN}✅ Ngrok is running${NC}"
    
    # Extract URLs
    N8N_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tunnel in data['tunnels']:
    if 'n8n' in tunnel['name']:
        print(tunnel['public_url'])
        break
" 2>/dev/null || echo "")

    API_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tunnel in data['tunnels']:
    if 'api' in tunnel['name']:
        print(tunnel['public_url'])
        break
" 2>/dev/null || echo "")

else
    echo -e "${YELLOW}⚠️ Ngrok starting...${NC}"
fi

# Display results
echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================"
echo ""
echo -e "${BLUE}📍 Local Access:${NC}"
echo "   • n8n Dashboard: http://localhost:5678"
echo "   • Mock API: http://localhost:8000"
echo "   • Ngrok Dashboard: http://localhost:4040"
echo "   • Monitoring: http://localhost:3001"
echo ""

if [ ! -z "$N8N_URL" ] || [ ! -z "$API_URL" ]; then
    echo -e "${BLUE}🌍 External Access (via ngrok):${NC}"
    [ ! -z "$N8N_URL" ] && echo "   • n8n Dashboard: $N8N_URL"
    [ ! -z "$API_URL" ] && echo "   • Mock API: $API_URL"
    echo ""
fi

echo -e "${BLUE}🔐 Authentication:${NC}"
echo "   • Username: $N8N_BASIC_AUTH_USER"
echo "   • Password: $N8N_BASIC_AUTH_PASSWORD"
echo ""

echo -e "${BLUE}💰 Cost Information:${NC}"
echo "   • Ngrok: FREE (with limits)"
echo "   • Mock APIs: $0.00"
echo "   • Cloud hosting: Varies by provider"
echo ""

echo -e "${BLUE}📋 Next Steps:${NC}"
echo "   1. Access n8n via the external URL"
echo "   2. Create your automation workflows"
echo "   3. Test with mock APIs (free)"
echo "   4. Add real API keys when ready"
echo ""

echo -e "${BLUE}🛠️ Management Commands:${NC}"
echo "   • View logs: docker-compose -f docker-compose.cloud.yml logs"
echo "   • Stop: docker-compose -f docker-compose.cloud.yml down"
echo "   • Restart: docker-compose -f docker-compose.cloud.yml restart"
echo ""

echo -e "${GREEN}✅ Your Instagram automation is now running in the cloud!${NC}"
echo "🌍 Access it from anywhere using the external URLs above"
