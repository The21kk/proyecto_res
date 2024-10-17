#!/bin/bash

# Este script instalará las dependencias necesarias y ejecutará el script de Python

# Actualizar el sistema
echo "Actualizando los repositorios de paquetes..."
sudo apt update

# Instalar pip si no está instalado
echo "Verificando si pip está instalado..."
if ! command -v pip &> /dev/null
then
    echo "pip no está instalado. Instalando pip..."
    sudo apt install python3-pip -y
else
    echo "pip ya está instalado."
fi

# Instalar las librerías necesarias usando pip
echo "Instalando las librerías necesarias..."
pip install requests pyproj geojson

# Verificar si el script Python existe
PYTHON_SCRIPT="stop.py"  # Cambia esto al nombre de tu script Python
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "El archivo $PYTHON_SCRIPT no se encuentra. Asegúrate de que el archivo esté en el mismo directorio que este script."
    exit 1
fi

# Ejecutar el script de Python
echo "Ejecutando el script de Python..."
python3 "$PYTHON_SCRIPT"

# Mensaje final
echo "Ejecución completada."

