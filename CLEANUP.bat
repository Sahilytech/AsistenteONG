@echo off
echo.
echo ====================================
echo LIMPIEZA COMPLETA DE CACHÉ
echo Asistente ONG v0.9
echo ====================================
echo.

echo Limpiando caché de Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
echo ✅ __pycache__ limpiado

echo.
echo Sincronizando con GitHub (reset duro)...
git fetch origin main
git reset --hard origin/main
echo ✅ Sincronizado

echo.
echo Limpiando archivos .pyc...
del /s /q *.pyc 2>nul
echo ✅ .pyc limpiado

echo.
echo ====================================
echo LISTO! Ahora ejecuta:
echo python -m src.main
echo ====================================
echo.
pause
