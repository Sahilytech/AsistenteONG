@echo off
REM Script para generar AsistenteONG.exe para distribuir en pendrives
REM Uso: Double-click o ejecutar en terminal

echo.
echo ====================================
echo Asistente ONG - Constructor .EXE
echo v0.8 PROFESIONAL
echo ====================================
echo.

REM Verificar si PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo.
echo Compilando ejecutable (esto puede tomar 1-2 minutos)...
echo.

REM Generar .exe
pyinstaller --onefile ^
    --windowed ^
    --icon=assets/logo_g.png ^
    --name AsistenteONG ^
    --distpath ./dist ^
    --buildpath ./build ^
    --specpath ./build ^
    src/main.py

echo.
if exist dist\AsistenteONG.exe (
    echo ✅ EXITO! Archivo generado:
    echo    dist\AsistenteONG.exe
    echo.
    echo Instrucciones para usar en pendrive:
    echo 1. Copia dist\AsistenteONG.exe a tu pendrive
    echo 2. Entrégalo a la ONG
    echo 3. Ellos hacen doble-click para ejecutar
    echo 4. Funciona 100% offline, sin instalar Python
    echo.
    pause
) else (
    echo ❌ ERROR: No se pudo generar el .exe
    echo Verifica los errores arriba
    pause
)
