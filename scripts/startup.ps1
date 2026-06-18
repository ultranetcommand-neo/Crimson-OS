# Crimson OS — local intranet bootstrap (Windows)
# Usage: .\scripts\startup.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Bridge = Join-Path $Root "Agent_Bridge"

if (-not (Test-Path $Bridge)) {
    Write-Error "Agent_Bridge not found at $Bridge"
}

$existing = docker ps -q --filter "name=crimson-intranet"
if ($existing) {
    Write-Host "Stopping existing crimson-intranet container..."
    docker stop crimson-intranet | Out-Null
    docker rm crimson-intranet | Out-Null
}

Write-Host "Starting Agent_Bridge intranet on http://127.0.0.1:8092 ..."
docker run -d --name crimson-intranet -p 8092:80 `
    -v "${Bridge}:/usr/share/nginx/html:ro" nginx

Write-Host "OK: Intranet live. Cockpit API :8093 is operator-local (not in this container)."
Write-Host "Health: .\scripts\health_check.ps1"