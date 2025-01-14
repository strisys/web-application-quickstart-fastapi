$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

Write-Host "Setting up virtual environment in $projectRoot"

# Function to safely remove virtual environment
function Remove-VirtualEnv {
    param (
        [string]$venvPath
    )
    
    try {
        # Deactivate virtual environment if it's active
        if (Test-Path Function:\deactivate) {
            deactivate
            Start-Sleep -Seconds 1  # Give time for deactivation
        }
        
        # Kill any running Python processes from this venv
        $pythonExePath = Join-Path $venvPath "Scripts\python.exe"
        if (Test-Path $pythonExePath) {
            $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | 
            Where-Object { $_.Path -eq $pythonExePath }
            if ($pythonProcesses) {
                $pythonProcesses | ForEach-Object { $_.Kill() }
                Start-Sleep -Seconds 1  # Give time for processes to end
            }
        }

        # Remove the directory with retry logic
        $maxAttempts = 3
        $attempt = 0
        $success = $false

        while (-not $success -and $attempt -lt $maxAttempts) {
            try {
                Remove-Item -Recurse -Force $venvPath -ErrorAction Stop
                $success = $true
            }
            catch {
                $attempt++
                if ($attempt -lt $maxAttempts) {
                    Write-Host "Attempt $attempt failed. Retrying in 2 seconds..."
                    Start-Sleep -Seconds 2
                }
                else {
                    throw $_
                }
            }
        }
    }
    catch {
        Write-Host "Error removing virtual environment: $_" -ForegroundColor Red
        Write-Host "Please close any applications or terminals using the virtual environment and try again." -ForegroundColor Yellow
        exit 1
    }
}

# Check if virtual environment exists and prompt for removal
if (Test-Path ".venv") {
    $response = Read-Host "Virtual environment already exists. Do you want to remove it? (Y/N)"
    if ($response.ToUpper() -eq 'Y') {
        Write-Host "Removing existing virtual environment..."
        Remove-VirtualEnv -venvPath (Join-Path $projectRoot ".venv")
        Write-Host "Existing virtual environment removed."
    }
    else {
        Write-Host "Script cancelled by user." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Creating virtual environment..."
try {
    python3 -m venv .venv
}
catch {
    Write-Host "Error creating virtual environment: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Activating virtual environment..."
try {
    .\.venv\Scripts\Activate.ps1
}
catch {
    Write-Host "Error activating virtual environment: $_" -ForegroundColor Red
    exit 1
}

# Check if requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    try {
        python -m pip install -r requirements.txt
    }
    catch {
        Write-Host "Error installing dependencies: $_" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "Error: requirements.txt not found in $projectRoot" -ForegroundColor Red
    exit 1
}

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Virtual environment is now activated and dependencies are installed."