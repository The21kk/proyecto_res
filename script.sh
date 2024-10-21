#!/bin/bash

# Define las rutas
DOWNLOADS_DIR="$HOME/Downloads"
AMENAZAS_DIR="$DOWNLOADS_DIR/amenazas"
METADATA_DIR="$DOWNLOADS_DIR/Metadata"
INFRAESTRUCTURA_DIR="$DOWNLOADS_DIR/infrastructure"
BD_SCRIPT="$DOWNLOADS_DIR/bdd.sql"  # Ruta al archivo bdd.sql

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
    echo "La carpeta 'amenazas' no existe en $DOWNLOADS_DIR."
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
    echo "La carpeta 'Metadata' no existe en $DOWNLOADS_DIR."
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
    echo "La carpeta 'infraestructura' no existe en $DOWNLOADS_DIR."
fi

# Ejecutar el script SQL para inicializar la base de datos
if [ -f "$BD_SCRIPT" ]; then
    echo "Ejecutando el script de inicialización de la base de datos bdd.sql..."
    psql -U postgres -f "$BD_SCRIPT"
else
    echo "El archivo bdd.sql no se encontró en $DOWNLOADS_DIR."
fi

echo "Ejecución de scripts finalizada."
