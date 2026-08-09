# Script de limpieza en PowerShell

Write-Host "`n===================================="
Write-Host "LIMPIEZA COMPLETA DE CACHÉ"
Write-Host "Asistente ONG v0.9"
Write-Host "====================================" -ForegroundColor Cyan

Write-Host "`nLimpiando caché de Python..."
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force 2>$null
Write-Host "✅ __pycache__ limpiado" -ForegroundColor Green

Write-Host "`nSincronizando con GitHub..."
git fetch origin main
git reset --hard origin/main
Write-Host "✅ Sincronizado" -ForegroundColor Green

Write-Host "`nLimpiando archivos .pyc..."
Get-ChildItem -Path . -Include *.pyc -Recurse | Remove-Item -Force 2>$null
Write-Host "✅ .pyc limpiado" -ForegroundColor Green

Write-Host "`n===================================="
Write-Host "LISTO! Ahora ejecuta:" -ForegroundColor Cyan
Write-Host "python -m src.main" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Cyan
