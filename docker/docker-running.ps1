# List of images for which you would like to count running containers
$images = @("microsoft/dotnet-samples","microsoft/powershell")

# To be able to run this script you need to add `powershell.exe c:\path\to\the\script.ps1` in the plugin configuration
$configuration = @"
{
    "maxruntime": 10000,
    "period": 60,
    "metrics": [{
        "id": 1,
        "datatype": "DOUBLE",
        "name": "Containers running",
        "description": "Amount of containers running for specific image",
        "groups": "Docker",
        "unit": "#",
        "tags": "",
        "calctype": "Instant",
	"dimensions": [
		{"id": 1, "name": "Image name"}
	]
    }]
}
"@

# Print configuration
if($args[0] -eq "-c") {
    Write-Host $configuration
}

# Print metrics
if($args[0] -eq "-d") {
    # Loop images
    Foreach ($image in $images)
    {
	# Retrieve number of containers running for image
	$running = (docker ps -q --format "{{.Image}}" | Select-String -Pattern "$image" | Measure-Object -Line).Lines
    	Write-Host "M1 ""1:$image"" $running"
    }

}
