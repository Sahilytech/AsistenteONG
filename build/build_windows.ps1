$ErrorActionPreference = 'Stop'

Set-Location (Split-Path $PSScriptRoot -Parent)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (Test-Path dist) { Remove-Item dist -Recurse -Force }
if (Test-Path build) { Remove-Item build -Recurse -Force }

python -m PyInstaller --noconfirm --clean --windowed --name AsistenteONG --icon assets/logo_g.png src/main.py

Write-Host "Build terminado: dist/AsistenteONG/AsistenteONG.exe"
