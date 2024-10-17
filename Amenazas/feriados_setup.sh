#!/bin/bash

# Archivo Python que contiene el código
PYTHON_SCRIPT="API_feriados.py"

# Verificar si pip está instalado, si no, instalarlo
if ! command -v pip &> /dev/null
then
    echo "pip no está instalado. Instalando pip..."
    sudo apt update
    sudo apt install python3-pip -y
else
    echo "pip ya está instalado."
fi

# Verificar si requests y pandas están instalados, si no, instalarlos
pip install requests pandas

# Ejecutar el script Python
if [ -f "$PYTHON_SCRIPT" ]; then
    echo "Ejecutando el script Python..."
    python3 "$PYTHON_SCRIPT"
else
    echo "El archivo $PYTHON_SCRIPT no existe. Verifica la ruta."
    exit 1
fi
