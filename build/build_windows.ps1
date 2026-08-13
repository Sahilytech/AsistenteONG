$ErrorActionPreference = 'Stop'

Set-Location (Split-Path $PSScriptRoot -Parent)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (Test-Path dist) { Remove-Item dist -Recurse -Force }
if (Test-Path build) { Remove-Item build -Recurse -Force }

python -m PyInstaller --noconfirm --clean --onefile --windowed --name AsistenteONG --add-data "assets;assets" --add-data "data;data" src/main.py

if (!(Test-Path "dist\AsistenteONG.exe")) {
    throw "No se generó dist\AsistenteONG.exe"
}

$size = (Get-Item "dist\AsistenteONG.exe").Length
if ($size -lt 1000000) {
    throw "El ejecutable parece inválido o demasiado pequeño: $size bytes"
}

Get-FileHash "dist\AsistenteONG.exe" -Algorithm SHA256 | Format-List
Write-Host "Build terminado: dist\AsistenteONG.exe"
