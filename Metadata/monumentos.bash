#!/bin/bash

# URL del servicio de características
URL="https://geoportalcmn.cl/server/rest/services/Geodatabasecorporativa/Puntos_Monumentos_Nacionales/FeatureServer/0/query?where=1%3D1&outFields=*&f=json"

# Ruta de destino para el archivo GeoJSON
DESTINO="$HOME/Desktop/U/proyecto_res/Metadata/obtener_metadata/monumentos_nacionales.geojson"

# Crear el directorio de destino si no existe
mkdir -p "$(dirname "$DESTINO")"

# Descargar los datos en formato JSON
echo "Descargando datos desde la URL..."
curl -o data.json "$URL"

# Verificar si la descarga fue exitosa
if [ $? -ne 0 ]; then
    echo "Error: La descarga falló."
    exit 1
fi

# Mostrar el tamaño del archivo descargado
echo "Tamaño del archivo descargado data.json:"
ls -lh data.json

# Convertir el JSON descargado a GeoJSON
echo "Convirtiendo JSON a GeoJSON..."
ogr2ogr -f "GeoJSON" "$DESTINO" data.json

# Verifica si el comando se ejecutó correctamente
if [ $? -eq 0 ]; then
    echo "Conversión a GeoJSON completada con éxito."
else
    echo "Hubo un error durante la conversión."
fi

# Limpia el archivo temporal
rm data.json
