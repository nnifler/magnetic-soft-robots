if (!(Test-Path -Path ".env")) {
    Write-Host "Necessary data for running the software is missing" -ForegroundColor DarkRed
    Write-Host "Consider running or re-running the install script (Install.ps1)" -ForegroundColor DarkRed
    return
}

get-content .env | ForEach-Object {
    $name, $value = $_.split('=')
    set-content env:\$name $value
}

if (!(Test-Path -Path $env:PYTHON_ROOT) -or !(Test-Path -Path $env:SOFA_ROOT)) {
    Write-Host "Necessary data for running the software is missing" -ForegroundColor DarkRed
    Write-Host "Consider running or re-running the install script (Install.ps1)" -ForegroundColor DarkRed
    return
}

& "$env:PYTHON_ROOT\python.exe" .\main.py
