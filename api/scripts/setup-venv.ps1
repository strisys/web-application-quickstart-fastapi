$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

Write-Host "Setting up virtual environment in $projectRoot"

# Check if virtual environment exists and prompt for removal
if (Test-Path ".venv") {
    $response = Read-Host "Virtual environment already exists. Do you want to remove it? (Y/N)"
    if ($response.ToUpper() -eq 'Y') {
        Write-Host "Removing existing virtual environment..."
        Remove-Item -Recurse -Force .venv
        Write-Host "Existing virtual environment removed."
    }
    else {
        Write-Host "Script cancelled by user." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Creating virtual environment..."
python3 -m venv .venv

Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# Check if requirements.txt exists
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    python -m pip install -r requirements.txt
}
else {
    Write-Host "Error: requirements.txt not found in $projectRoot" -ForegroundColor Red
    exit 1
}

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Virtual environment is now activated and dependencies are installed."