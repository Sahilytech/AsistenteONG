@echo off
setlocal
cd /d %~dp0

echo ==========================================
echo Asistente ONG - Ejecucion local
 echo ==========================================

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python no esta instalado o no esta en PATH.
  pause
  exit /b 1
)

if not exist .venv (
  echo Creando entorno virtual...
  python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR: no se pudieron instalar las dependencias.
  pause
  exit /b 1
)

python -m src.main
set ERR=%errorlevel%
call .venv\Scripts\deactivate.bat
if not "%ERR%"=="0" pause
exit /b %ERR%
