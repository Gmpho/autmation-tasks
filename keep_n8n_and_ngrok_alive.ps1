# PowerShell script to keep both ngrok and n8n (Docker) running and update .env with the latest public URL
# Run this script from your project root

$ngrokPath = "./ngrok.exe"
$envPath = ".env"
$dockerComposePath = "docker-compose.yml"
$containerName = "insta_automation"

function Get-NgrokUrl {
    try {
        $resp = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels"
        $url = $resp.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -ExpandProperty public_url
        return $url
    } catch {
        return $null
    }
}

function Update-EnvFile($url) {
    if (-not $url) { return }
    $envContent = Get-Content $envPath -Raw
    $envContent = $envContent -replace "N8N_EDITOR_BASE_URL=.*", "N8N_EDITOR_BASE_URL=$url"
    $envContent = $envContent -replace "WEBHOOK_URL=.*", "WEBHOOK_URL=$url"
    Set-Content $envPath $envContent
    Write-Host "[ngrok-keeper] Updated .env with new URL: $url" -ForegroundColor Green
}

function Ensure-Ngrok {
    if (-not (Get-Process ngrok -ErrorAction SilentlyContinue)) {
        Write-Host "[ngrok-keeper] Starting ngrok..." -ForegroundColor Yellow
        Start-Process -FilePath $ngrokPath -ArgumentList "http 5678" -WindowStyle Minimized
        Start-Sleep -Seconds 3
    }
}

function Ensure-N8n {
    $running = docker ps --filter "name=$containerName" --filter "status=running" -q
    if (-not $running) {
        Write-Host "[n8n-keeper] n8n is not running. Restarting via docker-compose..." -ForegroundColor Yellow
        docker-compose up -d
        Start-Sleep -Seconds 5
    }
}

$lastUrl = ""
while ($true) {
    Ensure-Ngrok
    Ensure-N8n
    $url = Get-NgrokUrl
    if ($url -and $url -ne $lastUrl) {
        Update-EnvFile $url
        $lastUrl = $url
    }
    Start-Sleep -Seconds 30
}