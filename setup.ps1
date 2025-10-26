# ===================================
# AMD AI Upscaler - Auto Setup
# ===================================

Write-Host "="*60 -ForegroundColor Cyan
Write-Host "AMD AI UPSCALER - AUTOMATIC SETUP" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

$projectPath = "C:\Quick-Access\Projects\AI-Upscaler"
Set-Location $projectPath

# Step 1: Check Python
Write-Host "`n[1/4] Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "  ✓ $pythonVersion" -ForegroundColor Green

# Step 2: Install dependencies
Write-Host "`n[2/4] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

$packages = @(
    "onnxruntime-directml",
    "numpy", 
    "pillow",
    "opencv-python",
    "mss"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    pip install $package --quiet
}

Write-Host "  ✓ All packages installed" -ForegroundColor Green

# Step 3: Verify ONNX Runtime DirectML
Write-Host "`n[3/4] Verifying DirectML support..." -ForegroundColor Yellow
$providers = python -c "import onnxruntime; print(','.join(onnxruntime.get_available_providers()))" 2>&1

if ($providers -match "DmlExecutionProvider") {
    Write-Host "  ✓ DirectML support confirmed (AMD GPU acceleration enabled)" -ForegroundColor Green
} else {
    Write-Host "  ⚠ DirectML not found, will use CPU (slower)" -ForegroundColor Yellow
}

# Step 4: List available models
Write-Host "`n[4/4] Available AI models:" -ForegroundColor Yellow
Get-ChildItem "$projectPath\models" -Filter "*.onnx" | ForEach-Object {
    $sizeMB = [math]::Round($_.Length/1MB, 2)
    Write-Host "  ✓ $($_.Name) ($sizeMB MB)" -ForegroundColor Gray
}

# Summary
Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "SETUP COMPLETE!" -ForegroundColor Green
Write-Host ("="*60) -ForegroundColor Cyan

Write-Host "`nYou can now:" -ForegroundColor White
Write-Host "  1. Test image upscaling:" -ForegroundColor Gray
Write-Host "     python upscaler.py test.jpg output.jpg`n" -ForegroundColor Gray
Write-Host "  2. Run real-time game upscaling:" -ForegroundColor Gray
Write-Host "     python game_upscaler.py`n" -ForegroundColor Gray

Write-Host "See INSTALL.md for more details." -ForegroundColor Gray

# Additional dependencies for daemon
Write-Host "`n[BONUS] Installing daemon dependencies..." -ForegroundColor Yellow
$daemonPackages = @("pystray", "keyboard", "psutil")

foreach ($package in $daemonPackages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    pip install $package --quiet
}

Write-Host "  ✓ Daemon packages installed" -ForegroundColor Green
