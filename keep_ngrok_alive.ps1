# PowerShell script to keep ngrok running and update .env with the latest public URL
# Run this script from your project root

$ngrokPath = "./ngrok.exe"
$envPath = ".env"

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

# Start ngrok if not running
if (-not (Get-Process ngrok -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $ngrokPath -ArgumentList "http 5678" -WindowStyle Minimized
    Start-Sleep -Seconds 3
}

$lastUrl = ""
while ($true) {
    $url = Get-NgrokUrl
    if ($url -and $url -ne $lastUrl) {
        Update-EnvFile $url
        $lastUrl = $url
    }
    Start-Sleep -Seconds 30
}
