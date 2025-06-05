# Define your API and App Registration
$clientId = "1b595ea9-866f-4abc-8d82-0304b58deb01"  # Replace with your App Registration's client ID
$scope = "api://$clientId/.default"
$baseUrl = "http://localhost:8080"  # Replace with your actual host
$endpoint = "/api/hello"
$url = "$baseUrl$endpoint"

# Fetch token using Azure CLI
$token = az account get-access-token --scope $scope --query accessToken -o tsv
Write-Host $token

# Prepare headers
$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/json"
}

# Make the request
Write-Host "Invoking ${url}"
$response = Invoke-RestMethod -Uri $url -Method GET -Headers $headers

# Display the result
Write-Host "API Response:"
$response | ConvertTo-Json -Depth 5
