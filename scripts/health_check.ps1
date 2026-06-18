# Crimson OS — minimal health check
# Usage: .\scripts\health_check.ps1

$ErrorActionPreference = "Continue"
$ok = $true

function Test-Endpoint($Name, $Url) {
    try {
        $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 400) {
            Write-Host "[OK] $Name — $Url"
        } else {
            Write-Host "[FAIL] $Name — HTTP $($r.StatusCode)"
            $script:ok = $false
        }
    } catch {
        Write-Host "[FAIL] $Name — $($_.Exception.Message)"
        $script:ok = $false
    }
}

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "=== Crimson OS Health Check ==="

Test-Endpoint "Intranet (Agent_Bridge)" "http://127.0.0.1:8092/Node_0.md"
Test-Endpoint "Cockpit API (optional)" "http://127.0.0.1:8093/status"

$proof = Join-Path $Root "Geometric_Unity_Validation\proof.md"
if (Test-Path $proof) { Write-Host "[OK] proof.md present" } else { Write-Host "[FAIL] proof.md missing"; $ok = $false }

$ablation = Join-Path $Root "Geometric_Unity_Validation\jhtdb_ablation_results.json"
if (Test-Path $ablation) { Write-Host "[OK] jhtdb_ablation_results.json present" } else { Write-Host "[FAIL] ablation results missing"; $ok = $false }

python (Join-Path $Root "scripts\verify_research_artifacts.py")
if ($LASTEXITCODE -ne 0) { $ok = $false }

if ($ok) {
    Write-Host "=== PASS ==="
    exit 0
} else {
    Write-Host "=== FAIL (see above) ==="
    exit 1
}