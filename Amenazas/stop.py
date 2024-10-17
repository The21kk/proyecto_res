import requests
import json
import csv
from pyproj import Transformer
import geojson

# URL base del servicio WMS
wms_url = "https://stop.carabineros.cl/geoserver/stop/wms"

geojson_path = '../Metadata/museos.geojson'

# Leer el archivo GeoJSON
with open(geojson_path, 'r', encoding='utf-8') as f:
    gj = geojson.load(f)

# Definir el transformador entre EPSG:4326 y EPSG:3857
transformer = Transformer.from_crs("epsg:4326", "epsg:3857")

# Parámetros comunes para todas las solicitudes WMS
params = {
    'service': 'WMS',
    'request': 'GetFeatureInfo',
    'version': '1.1.1',
    'layers': 'stop:Robos',
    'styles': '',
    'format': 'image/png',
    'transparent': 'true',
    'info_format': 'application/json',
    'srs': 'EPSG:3857',
    'width': '1920',
    'height': '936',
    'query_layers': 'stop:Robos'
}

def extract_coordinates(geometry):
    if geometry['type'] == 'Point':
        return [geometry['coordinates']]
    elif geometry['type'] in ['MultiPoint', 'LineString']:
        return geometry['coordinates']
    elif geometry['type'] in ['Polygon', 'MultiLineString']:
        return [coord for part in geometry['coordinates'] for coord in part]
    elif geometry['type'] == 'MultiPolygon':
        return [coord for part in geometry['coordinates'] for ring in part for coord in ring]
    else:
        return []

# Función para hacer una petición GetFeatureInfo para un punto específico
def get_feature_info(point):
    # Actualiza los parámetros con el bbox y las coordenadas del punto
    params.update({
        'bbox': ','.join(map(str, point['bbox'])),
        'X': point['x'],
        'Y': point['y']
    })
    
    # Realizar la solicitud GET al servicio WMS
    response = requests.get(wms_url, params=params)
    
    # Verificar si la respuesta es exitosa
    if response.status_code == 200:
        try:
            return response.json()  # Devolver la respuesta en formato JSON
        except requests.exceptions.JSONDecodeError:
            print("Error: La respuesta no es un JSON válido.")
            print(response.text)
            return None
    else:
        print(f"Error en la solicitud para el punto {point['x']}, {point['y']}: {response.status_code}")
        return None

# Escribir los resultados en un archivo CSV
with open('robos.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Lat', 'Lon', 'Robos'])

    for feature in gj['features']:
        geometry = feature['geometry']
        coordinates = extract_coordinates(geometry)

        if len(coordinates) > 0:
            Latitud = float(coordinates[0][1])
            Longitud = float(coordinates[0][0])
     

            # Transformar las coordenadas de EPSG:4326 a EPSG:3857
            NewLong, NewLat = transformer.transform(Latitud, Longitud)

            buffer_x=-2293.11
            buffer_y=-1117.89

            point = {'x': 0, 'y': 0, 'bbox': [NewLong,NewLat,NewLong-buffer_x,NewLat-buffer_y]}
        
            feature_info = get_feature_info(point)

            if feature_info and "features" in feature_info and len(feature_info["features"]) > 0:
                robos = feature_info["features"][0]["properties"].get("robos", "N/A")
                writer.writerow([Latitud, Longitud, json.dumps(robos)])
            elif feature_info and "totalFeatures" in feature_info and feature_info["totalFeatures"] == 'unknown':
                writer.writerow([Latitud, Longitud, "0"])

