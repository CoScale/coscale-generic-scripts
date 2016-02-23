# To be able to run this script you need to add `powershell.exe c:\path\to\the\script.ps1` in the plugin configuration
$configuration = @"
{
    "maxruntime": 10000,
    "metrics": [{
        "id": 1,
        "datatype": "DOUBLE",
        "name": "Application Errors",
        "description": "Amount of errors in the 'Application' event log",
        "groups": "Custom Metrics",
        "unit": "errors",
        "calctype": "Difference"
    }]
}
"@

# Print configuration
if($args[0] -eq "-c") {
    Write-Host $configuration
}

# Print metrics
if($args[0] -eq "-d") {
    $errors =  (Get-EventLog -log application -Newest 1000 | select-string -inputobject {$_.message} -pattern "failed" | Measure-Object -Line).Lines
    Write-Host M1 $errors 
}

