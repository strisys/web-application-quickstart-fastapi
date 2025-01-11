$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
Set-Location ..

.\.venv\Scripts\python.exe -m uvicorn src.app:app --reload --port 8080