# ===================================
# AI Upscaler - Auto-Start Service
# ===================================

param(
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Status
)

$projectPath = "C:\Quick-Access\Projects\AI-Upscaler"
$taskName = "AIUpscalerDaemon"
$pythonExe = (Get-Command python).Source
$scriptPath = "$projectPath\daemon.py"

function Install-Service {
    Write-Host "Installing AI Upscaler service..." -ForegroundColor Cyan
    
    # Create scheduled task that runs at startup
    $action = New-ScheduledTaskAction -Execute $pythonExe -Argument $scriptPath -WorkingDirectory $projectPath
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
    
    Write-Host "✓ Service installed" -ForegroundColor Green
    Write-Host "  Task name: $taskName" -ForegroundColor Gray
    Write-Host "  Will start automatically at login" -ForegroundColor Gray
}


function Uninstall-Service {
    Write-Host "Uninstalling AI Upscaler service..." -ForegroundColor Cyan
    
    try {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "✓ Service uninstalled" -ForegroundColor Green
    } catch {
        Write-Host "Service not found or already uninstalled" -ForegroundColor Yellow
    }
}

function Start-Service {
    Write-Host "Starting AI Upscaler daemon..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $taskName
    Write-Host "✓ Daemon started" -ForegroundColor Green
    Write-Host "  Check system tray for icon" -ForegroundColor Gray
    Write-Host "  Press Ctrl+Alt+U to toggle" -ForegroundColor Gray
}

function Stop-Service {
    Write-Host "Stopping AI Upscaler daemon..." -ForegroundColor Cyan
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    # Kill Python process if still running
    Get-Process python -ErrorAction SilentlyContinue | 
        Where-Object {$_.CommandLine -like "*daemon.py*"} | 
        Stop-Process -Force -ErrorAction SilentlyContinue
    
    Write-Host "✓ Daemon stopped" -ForegroundColor Green
}

function Get-ServiceStatus {
    Write-Host "AI Upscaler Service Status" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Gray
    
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    if ($task) {
        Write-Host "Installed: YES" -ForegroundColor Green
        Write-Host "State: $($task.State)" -ForegroundColor $(if ($task.State -eq "Running") {"Green"} else {"Yellow"})
        
        # Check if process is running
        $process = Get-Process python -ErrorAction SilentlyContinue | 
            Where-Object {$_.CommandLine -like "*daemon.py*"}
        
        if ($process) {
            Write-Host "Process: RUNNING (PID: $($process.Id))" -ForegroundColor Green
        } else {
            Write-Host "Process: NOT RUNNING" -ForegroundColor Yellow
        }
        
        # Check upscaler state
        $configPath = "$projectPath\daemon_config.txt"
        if (Test-Path $configPath) {
            $state = Get-Content $configPath
            Write-Host "Upscaling: $state" -ForegroundColor $(if ($state -eq "enabled") {"Green"} else {"Gray"})
        }
    } else {
        Write-Host "Installed: NO" -ForegroundColor Red
        Write-Host "Run: .\service.ps1 -Install" -ForegroundColor Gray
    }
}

# Main logic
if ($Install) { Install-Service }
elseif ($Uninstall) { Uninstall-Service }
elseif ($Start) { Start-Service }
elseif ($Stop) { Stop-Service }
elseif ($Status) { Get-ServiceStatus }
else {
    Write-Host "AI Upscaler Service Manager" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Gray
    Write-Host "`nUsage:"
    Write-Host "  .\service.ps1 -Install    Install auto-start service"
    Write-Host "  .\service.ps1 -Start      Start daemon now"
    Write-Host "  .\service.ps1 -Stop       Stop daemon"
    Write-Host "  .\service.ps1 -Status     Check status"
    Write-Host "  .\service.ps1 -Uninstall  Remove service`n"
}
