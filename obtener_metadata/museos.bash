#!/bin/bash

# URL del servicio GeoJSON de Museos
URL="https://geoportalcmn.cl/server/rest/services/Geodatabasecorporativa/Museos/FeatureServer/0/query"

# Parámetros para solicitar el archivo en formato GeoJSON
PARAMS="?where=1%3D1&outFields=*&f=geojson"

# Descargar el archivo GeoJSON
curl -o museos.geojson "${URL}${PARAMS}"

echo "Descarga completada: museos.geojson"                                      