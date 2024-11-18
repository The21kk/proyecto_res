#!/bin/bash

# Define la ruta principal como la ubicación actual del script y conviértela en una ruta absoluta
BASE_DIR="$(realpath "$(dirname "$0")")"

# Define las rutas de las carpetas y el archivo SQL usando la ruta base
AMENAZAS_DIR="$BASE_DIR/Amenazas"
METADATA_DIR="$BASE_DIR/Metadata"
INFRAESTRUCTURA_DIR="$BASE_DIR/Infraestructura"
BD_SCRIPT="$BASE_DIR/bdd.sql"

# Ejecutar scripts en la carpeta 'Amenazas'
if [ -d "$AMENAZAS_DIR" ]; then
    echo "Ejecutando scripts en la carpeta 'Amenazas'..."
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
    echo "La carpeta 'Amenazas' no existe en $BASE_DIR."
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

    # Ejecutar opa.py después de los scripts de 'Metadata'
    if [ -f "opa.py" ]; then
        echo "Ejecutando opa.py..."
        python3 opa.py
        if [ $? -ne 0 ]; then
            echo "Error al ejecutar opa.py."
            exit 1
        fi
    else
        echo "El archivo opa.py no se encontró en $METADATA_DIR."
    fi
else
    echo "La carpeta 'Metadata' no existe en $BASE_DIR."
fi

# Ejecutar scripts en la carpeta 'Infraestructura'
if [ -d "$INFRAESTRUCTURA_DIR" ]; then
    echo "Ejecutando scripts en la carpeta 'Infraestructura'..."
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
    echo "La carpeta 'Infraestructura' no existe en $BASE_DIR."
fi

# Ejecutar el script SQL para inicializar la base de datos
if [ -f "$BD_SCRIPT" ]; then
    echo "Ejecutando el script de inicialización de la base de datos bdd.sql..."
    psql -U boris -d edges_sql -f "$BD_SCRIPT"
else
    echo "El archivo bdd.sql no se encontró en $BASE_DIR."
fi

# Ejecutar prob_ame.py en la raíz del proyecto
if [ -f "$BASE_DIR/prob_ame.py" ]; then
    echo "Ejecutando prob_ame.py..."
    python3 "$BASE_DIR/prob_ame.py"
    if [ $? -ne 0 ]; then
        echo "Error al ejecutar prob_ame.py."
        exit 1
    fi
else
    echo "El archivo prob_ame.py no se encontró en $BASE_DIR."
fi

echo "Ejecución de scripts finalizada."
