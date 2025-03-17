$py_version = "3.10.11"

$arch = "amd64"
$sofa_version = "v24.06.00"
$sofa_arch = "Win64"
$sofa_url = "https://github.com/sofa-framework/sofa/releases/download/$sofa_version/SOFA_${sofa_version}_$sofa_arch.zip"
$sofa_archive = "sofa-$sofa_version-$sofa_arch.zip"
$sofa_path = "SOFA_${sofa_version}_$sofa_arch"
$py_url = "https://www.python.org/ftp/python/$py_version/python-$py_version-embed-$arch.zip"
$get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
$py_archive = "python-$py_version-$arch.zip"
$py_path = "python-$py_version-$arch"

$global:ProgressPreference = 'SilentlyContinue'
$py_version_a, $py_version_b, $py_version_c = $py_version.split(".")
function Save-EnvFile {
    param (
        [string]$FilePath = "env.txt",
        [string[]]$VariableNames
    )

    $content = @()
    foreach ($varName in $VariableNames) {
        $value = Get-Variable -Name $varName -ErrorAction SilentlyContinue
        if ($value) {
            $content += "$($varName.ToUpper())=$($value.Value)"
        }
    }

    $content | Out-File -Encoding UTF8 -FilePath $FilePath
    Write-Host "Environment variables saved to $FilePath"
}

if ((Test-Path -Path $py_archive) -or (Test-Path -Path $py_path) -or (Test-Path -Path $sofa_archive) -or (Test-Path -Path $sofa_path) -or (Test-Path -Path "get_pip.py") -or (Test-Path -Path ".env")) {
    Write-Host "The software is either already installed or a directory / file would be overridden by this install script" -ForegroundColor DarkRed
    Write-Host "Aborting installation!" -ForegroundColor DarkRed
    return
}

Write-Output "Downloading Python $py_version"
Invoke-WebRequest -uri $py_url -Method "GET" -Outfile $py_archive
Expand-Archive -Path $py_archive -DestinationPath $py_path

Write-Output "Downloading SOFA $sofa_version"
Invoke-WebRequest -uri $sofa_url -Method "GET" -Outfile $sofa_archive
Expand-Archive -Path $sofa_archive -DestinationPath .

Invoke-WebRequest -uri $get_pip_url -Method "GET" -Outfile get_pip.py
& "$py_path/python.exe" get_pip.py --no-warn-script-location

$pthFile = "$py_path\python$py_version_a$py_version_b._pth"
Add-Content -Path $pthFile -Value "$pwd\$py_path\Lib\site-packages"
Add-Content -Path $pthFile -Value "$pwd\$sofa_path\plugins\STLIB\lib\python3\site-packages"
Add-Content -Path $pthFile -Value "$pwd\$sofa_path\plugins\SofaPython3\lib\python3\site-packages"
Add-Content -Path $pthFile -Value "$pwd"
& "$py_path\python.exe" -m pip install -r requirements.txt --no-warn-script-location

$sofa_root = "$pwd\$sofa_path"
$python_root = "$pwd\$py_path"

Save-EnvFile -FilePath .env -VariableNames @("sofa_root", "python_root")

Write-Host "Installation finished!" -ForegroundColor DarkGreen
Write-Host "Execute the software by running Run.ps1" -ForegroundColor DarkGreen
