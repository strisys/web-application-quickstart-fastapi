# Get the directory where the script is located
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "Building Docker image..."
docker build -t lions-api -f ../Dockerfile ..

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed."
    exit $LASTEXITCODE
}

Write-Host "Docker build succeeded."
$response = Read-Host "Do you want to run the container? (Y/n)"

if ($response -eq '' -or $response -eq 'y' -or $response -eq 'Y') {
    Write-Host "Stopping any existing containers using lions-api image..."
    docker ps -q --filter ancestor=lions-api | ForEach-Object { docker stop $_ }

    Write-Host "Running Docker container..."
    Start-Process "http://localhost:8080/api/data"
    docker run --rm -p 8080:8080 lions-api
}
