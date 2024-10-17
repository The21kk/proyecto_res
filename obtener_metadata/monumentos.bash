#!/bin/bash

# URL del servicio de características
URL="https://geoportalcmn.cl/server/rest/services/Geodatabasecorporativa/Puntos_Monumentos_Nacionales/FeatureServer/0/query?where=1%3D1&outFields=*&f=json"

# Ruta de destino para el archivo GeoJSON
DESTINO="$HOME/Desktop/obtener_metadata/monumentos_nacionales.geojson"

# Descargar los datos en formato JSON
curl -o data.json "$URL"

# Convertir el JSON descargado a GeoJSON
ogr2ogr -f "GeoJSON" "$DESTINO" data.json

# Verifica si el comando se ejecutó correctamente
if [ $? -eq 0 ]; then
    echo "Conversión a GeoJSON completada con éxito."
else
    echo "Hubo un error durante la conversión."
fi

# Limpia el archivo temporal
rm data.json
