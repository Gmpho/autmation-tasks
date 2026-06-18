#!/usr/bin/env bash
set -e

case "${1:-help}" in
  api)
    echo "🚀 Starting FastAPI server..."
    cd "$(dirname "$0")"
    source venv/bin/activate
    uvicorn mock_api_server:app --host 0.0.0.0 --port 8000 --reload
    ;;
  frontend)
    echo "🎨 Starting Vite dev server..."
    cd "$(dirname "$0")/frontend"
    npm run dev
    ;;
  n8n)
    echo "🐳 Starting n8n via Docker..."
    cd "$(dirname "$0")"
    docker compose up -d
    echo "🌐 n8n: http://localhost:5678"
    ;;
  build)
    echo "🏗️  Building frontend..."
    cd "$(dirname "$0")/frontend"
    npm run build
    echo "✅ Built to frontend/dist/"
    ;;
  test)
    echo "🧪 Running tests..."
    cd "$(dirname "$0")"
    source venv/bin/activate
    python test_mock_api.py
    ;;
  *)
    echo "Usage: $0 {api|frontend|n8n|build|test}"
    echo ""
    echo "  api       — Start FastAPI backend (port 8000)"
    echo "  frontend  — Start Vite dev server (port 5173)"
    echo "  n8n       — Start n8n via Docker (port 5678)"
    echo "  build     — Build frontend for production"
    echo "  test      — Run API tests"
    ;;
esac
