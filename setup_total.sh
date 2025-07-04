#!/bin/bash

# Versión de Python que quieres usar
PYTHON_VERSION="3.9.13"

echo "🕵️‍♂️ Verificando pyenv..."

if ! command -v pyenv &> /dev/null
then
    echo "🚀 pyenv no está instalado. Instalando con Homebrew..."
    brew update
    brew install pyenv
else
    echo "✅ pyenv ya está instalado."
fi

# Configurar pyenv en la sesión actual (esto puede variar según shell)
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# Verificar si la versión de Python ya está instalada
if pyenv versions --bare | grep -q "^$PYTHON_VERSION\$"; then
    echo "✅ Python $PYTHON_VERSION ya está instalado."
else
    echo "⬇️ Instalando Python $PYTHON_VERSION..."
    pyenv install $PYTHON_VERSION
fi

echo "🔧 Configurando la versión local de Python..."
pyenv local $PYTHON_VERSION

echo "🐍 Creando entorno virtual..."
python -m venv venv

echo "⚡ Activando entorno virtual..."
source venv/bin/activate

echo "📦 Actualizando pip..."
pip install --upgrade pip

echo "📥 Instalando dependencias..."
pip install opencv-python cvzone djitellopy mediapipe numpy

echo "✅ Todo listo para usar."
echo "👉 Ejecuta: source venv/bin/activate"
echo "👉 Y luego: python drone_hand.py"
