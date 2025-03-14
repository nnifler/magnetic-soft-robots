$py_version = "3.12.9"
$arch = "amd64"
$sofa_version = "v24.12.00"
$sofa_arch = "Win64"
$sofa_url = "https://github.com/sofa-framework/sofa/releases/download/$sofa_version/SOFA_${sofa_version}_$sofa_arch.zip"
$sofa_archive = "sofa-$sofa_version-$sofa_arch.zip"
$sofa_path = "sofa_${sofa_version}_$sofa_arch"
$py_url = "https://www.python.org/ftp/python/$py_version/python-$py_version-embed-$arch.zip"
$get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
$py_archive = "python-$py_version-$arch.zip"
$py_path = "python-$py_version-$arch"

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

# Invoke-WebRequest -uri $py_url -Method "GET" -Outfile $py_archive
Expand-Archive -Path $py_archive -DestinationPath $py_path

# Invoke-WebRequest -uri $sofa_url -Method "GET" -Outfile $sofa_archive
Expand-Archive -Path $sofa_archive -DestinationPath .

# Invoke-WebRequest -uri $get_pip_url -Method "GET" -Outfile get_pip.py
& "$py_path/python.exe" get_pip.py

# git clone --depth 1


$sofa_root = "$sofa_path"
$python_path = "$sofa_path/STLIB/lib/python3/site-packages:$sofa_path/SofaPython3/lib/python3/site-packages"
$python_root = "$py_path"

Save-EnvFile -FilePath .env -VariableNames @("sofa_root", "python_path", "python_root")
