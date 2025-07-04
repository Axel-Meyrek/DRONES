@echo off
:: setup_total.bat - Instalador para entorno Python en Windows

SET "PYTHON_VERSION=3.9.13"
SET "PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
SET "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%"

echo 🔍 Verificando si Python %PYTHON_VERSION% ya está instalado...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python no está instalado. Descargando instalador...
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
    echo 📦 Ejecutando instalador de Python...
    %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    echo ✅ Python instalado.
) ELSE (
    echo ✅ Python ya está instalado.
)

echo 🐍 Creando entorno virtual...
python -m venv venv

echo ⚡ Activando entorno virtual...
call venv\Scripts\activate.bat

echo ⬆️ Actualizando pip...
python -m pip install --upgrade pip

echo 📦 Instalando dependencias...
pip install opencv-python cvzone djitellopy mediapipe numpy

echo ✅ Entorno configurado con éxito.
echo Ejecuta:
echo   call venv\Scripts\activate.bat
echo   python drone_hand.py
