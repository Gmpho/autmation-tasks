#!/bin/bash
# Bash script to keep ngrok running and update .env with the latest public URL
# Also monitors and restarts n8n (Docker) if needed
# Run this script from your project root on Linux or macOS

NGROK_PATH="./ngrok"
ENV_PATH=".env"
CONTAINER_NAME="insta_automation"

get_ngrok_url() {
    curl -s http://localhost:4040/api/tunnels | \
        grep -o '"public_url":"https:[^"]*' | \
        sed 's/"public_url":"//'
}

update_env_file() {
    local url="$1"
    if [ -z "$url" ]; then return; fi
    sed -i "s|^N8N_EDITOR_BASE_URL=.*|N8N_EDITOR_BASE_URL=$url|" "$ENV_PATH"
    sed -i "s|^WEBHOOK_URL=.*|WEBHOOK_URL=$url|" "$ENV_PATH"
    echo "[ngrok-keeper] Updated .env with new URL: $url"
}

ensure_ngrok() {
    if ! pgrep -f "$NGROK_PATH http 5678" > /dev/null; then
        echo "[ngrok-keeper] Starting ngrok..."
        nohup $NGROK_PATH http 5678 > /dev/null 2>&1 &
        sleep 3
    fi
}

ensure_n8n() {
    if ! docker ps --filter "name=$CONTAINER_NAME" --filter "status=running" -q | grep . > /dev/null; then
        echo "[n8n-keeper] n8n is not running. Restarting via docker-compose..."
        docker-compose up -d
        sleep 5
    fi
}

last_url=""
while true; do
    ensure_ngrok
    ensure_n8n
    url=$(get_ngrok_url)
    if [ -n "$url" ] && [ "$url" != "$last_url" ]; then
        update_env_file "$url"
        last_url="$url"
    fi
    sleep 30
done
