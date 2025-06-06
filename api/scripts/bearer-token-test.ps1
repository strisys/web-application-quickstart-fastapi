$clientId = ""                       # Replace with your App Registration's client ID
$scope = "api://$clientId/.default"
$baseUrl = "http://localhost:8080"   # Replace with your actual host
$endpoint = "/api/hello"
$url = "$baseUrl$endpoint"

# Fetch token using Azure CLI
$token = az account get-access-token --scope $scope --query accessToken -o tsv
Write-Host $token

$headers = @{
  "Authorization" = "Bearer $token"
  "Accept" = "application/json"
}

Write-Host "Invoking ${url}"
$response = Invoke-RestMethod -Uri $url -Method GET -Headers $headers

Write-Host "API Response:"
$response | ConvertTo-Json -Depth 5
