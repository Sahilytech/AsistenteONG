@echo off
setlocal
cd /d %~dp0

echo ====================================
echo Asistente ONG - Constructor .EXE
echo ====================================

python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

python -m PyInstaller --noconfirm --clean --onefile --windowed --name AsistenteONG --icon=assets/logo_g.png --add-data "assets;assets" --add-data "data;data" src/main.py

if exist dist\AsistenteONG.exe (
  echo.
  echo EXITO: dist\AsistenteONG.exe
  echo Listo para pruebas y distribucion offline.
) else (
  echo ERROR: no se pudo generar el EXE.
  exit /b 1
)
endlocal
