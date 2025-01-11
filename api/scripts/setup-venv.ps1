$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

Write-Host "Setting up virtual environment in $projectRoot"

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python3 -m venv .venv
} else {
    Write-Host "Virtual environment already exists"
}

Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# Check if requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    python -m pip install -r requirements.txt
} else {
    Write-Host "Error: requirements.txt not found in $projectRoot" -ForegroundColor Red
    exit 1
}

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Virtual environment is now activated and dependencies are installed."