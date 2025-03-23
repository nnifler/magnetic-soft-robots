# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ #
#                        MSR, Magnetic Soft Robotics Simulation                        #
#   Copyright (C) 2025 Julius Hahnewald, Heiko Hellkamp, Finn Schubert, Carla Wehner   #
#                                                                                      #
# This program is free software; you can redistribute it and/or                        #
# modify it under the terms of the GNU Lesser General Public                           #
# License as published by the Free Software Foundation; either                         #
# version 2.1 of the License, or (at your option) any later version.                   #
#                                                                                      #
# This program is distributed in the hope that it will be useful,                      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU                    #
# Lesser General Public License for more details.                                      #
#                                                                                      #
# You should have received a copy of the GNU Lesser General Public                     #
# License along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301            #
# USA                                                                                  #
# ------------------------------------------------------------------------------------ #
# Contact information: finn.s.schubert@gmail.com                                       #
# ____________________________________________________________________________________ #

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
