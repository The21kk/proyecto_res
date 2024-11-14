#!/bin/bash

# Define la ruta principal como la ubicación actual del script y conviértela en una ruta absoluta
BASE_DIR="$(realpath "$(dirname "$0")")"

# Define las rutas de las carpetas y el archivo SQL usando la ruta base
AMENAZAS_DIR="$BASE_DIR/Amenazas"
METADATA_DIR="$BASE_DIR/Metadata"
INFRAESTRUCTURA_DIR="$BASE_DIR/Infraestructura"
BD_SCRIPT="$BASE_DIR/bdd.sql"

# Ejecutar scripts en la carpeta 'amenazas'
if [ -d "$AMENAZAS_DIR" ]; then
    echo "Ejecutando scripts en la carpeta 'amenazas'..."
    cd "$AMENAZAS_DIR" || exit

    for script in feriados_setup.sh metro_setup.sh stop_setup.sh trafico_setup.sh; do
        if [ -f "$script" ]; then
            echo "Ejecutando $script..."
            ./"$script"
        else
            echo "El script $script no se encontró en $AMENAZAS_DIR."
        fi
    done
else
    echo "La carpeta 'amenazas' no existe en $BASE_DIR."
fi

# Ejecutar scripts en la carpeta 'Metadata'
if [ -d "$METADATA_DIR" ]; then
    echo "Ejecutando scripts en la carpeta 'Metadata'..."
    cd "$METADATA_DIR" || exit

    for script in museos.bash monumentos.bash museos_setup.sh; do
        if [ -f "$script" ]; then
            echo "Ejecutando $script..."
            ./"$script"
        else
            echo "El script $script no se encontró en $METADATA_DIR."
        fi
    done
else
    echo "La carpeta 'Metadata' no existe en $BASE_DIR."
fi

# Ejecutar scripts en la carpeta 'infraestructura'
if [ -d "$INFRAESTRUCTURA_DIR" ]; then
    echo "Ejecutando scripts en la carpeta 'infraestructura'..."
    cd "$INFRAESTRUCTURA_DIR" || exit

    for script in cargar_monumentos.sh cargar_museos.sh; do
        if [ -f "$script" ]; then
            echo "Ejecutando $script..."
            ./"$script"
        else
            echo "El script $script no se encontró en $INFRAESTRUCTURA_DIR."
        fi
    done
else
    echo "La carpeta 'infraestructura' no existe en $BASE_DIR."
fi

# Ejecutar el script SQL para inicializar la base de datos
if [ -f "$BD_SCRIPT" ]; then
    echo "Ejecutando el script de inicialización de la base de datos bdd.sql..."
    psql -U boris -d edges_sql -f "$BD_SCRIPT"
else
    echo "El archivo bdd.sql no se encontró en $BASE_DIR."
fi

echo "Ejecución de scripts finalizada."
