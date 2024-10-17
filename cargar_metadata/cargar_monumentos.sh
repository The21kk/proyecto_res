#!/bin/bash

# Variables de configuración
DB_NAME="monumentos_db"             # Nombre de la base de datos
DB_USER="boris"                     # Usuario de PostgreSQL
DB_PASSWORD="2569"  # Contraseña del usuario
GEOJSON_PATH="$HOME/Desktop/obtener_metadata/monumentos_nacionales.geojson"  # Ruta del archivo GeoJSON
DB_TABLE="monumentos"               # Nombre de la tabla para cargar los datos

# Verificar si el archivo GeoJSON existe
if [ ! -f "$GEOJSON_PATH" ]; then
    echo "El archivo $GEOJSON_PATH no existe. Verifica la ruta."
    exit 1
fi

# Crear la base de datos (si no existe)
echo "Creando la base de datos $DB_NAME..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"

# Habilitar la extensión PostGIS en la base de datos
echo "Habilitando PostGIS en $DB_NAME..."
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Cargar los datos del GeoJSON a la tabla
echo "Cargando datos desde $GEOJSON_PATH a la tabla $DB_TABLE..."
ogr2ogr -f "PostgreSQL" \
  PG:"dbname=$DB_NAME user=$DB_USER password=$DB_PASSWORD" \
  "$GEOJSON_PATH" -nln $DB_TABLE -overwrite

# Verificar si la carga fue exitosa
if [ $? -eq 0 ]; then
    echo "Datos cargados exitosamente en la tabla $DB_TABLE."
else
    echo "Error en la carga de datos."
    exit 1
fi

# Imprimir las tablas de la base de datos
echo "Listando las tablas en la base de datos $DB_NAME:"
sudo -u postgres psql -d $DB_NAME -c "\dt"
