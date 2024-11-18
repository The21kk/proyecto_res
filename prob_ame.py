import pandas as pd
import geopandas as gpd

# Cargar el archivo GeoJSON (capa1)
geojson_file = './pagweb/data/capa1.geojson'
museos_gdf = gpd.read_file(geojson_file)

# Crear un diccionario para mapear nombres de museos a sus coordenadas
museos_coords = {
    row['nombre']: (row.geometry.y, row.geometry.x)  # Usamos 'geometry.y' y 'geometry.x' para latitud y longitud
    for _, row in museos_gdf.iterrows()
}


# Inicializar lista para almacenar probabilidades
probabilidades = []

# 1. Procesar `robos.csv` (tiene coordenadas directas)
robos_df = pd.read_csv('./Amenazas/robos.csv')
for _, row in robos_df.iterrows():
    probabilidad = min(row['Robos'] / 10, 1)  # Normalizar robos a [0, 1]
    probabilidades.append({
        'lat': row['Lat'],
        'lon': row['Lon'],
        'amenaza': 'Robo',
        'probabilidad': probabilidad
    })

# 2. Procesar `reportes_trafico.csv` (sin coordenadas, asociar a museos genéricamente)
trafico_df = pd.read_csv('./Amenazas/reportes_trafico.csv')
for _, row in trafico_df.iterrows():
    # Usar una ubicación genérica para reportes de tráfico
    lat, lon = -33.4489, -70.6693  # Coordenadas de Santiago
    probabilidad = 0.5  # Probabilidad constante (puedes ajustar)
    probabilidades.append({
        'lat': lat,
        'lon': lon,
        'amenaza': 'Reporte de Tráfico',
        'probabilidad': probabilidad
    })

# 3. Procesar `feriados_chile2024.csv` (sin coordenadas, ubicación genérica)
feriados_df = pd.read_csv('./Amenazas/feriados_chile2024.csv')
for _, row in feriados_df.iterrows():
    lat, lon = -33.4489, -70.6693  # Coordenadas de Santiago
    probabilidad = 0.5 if row['irrenunciable'] == 1 else 0.2
    probabilidades.append({
        'lat': lat,
        'lon': lon,
        'amenaza': 'Feriado',
        'probabilidad': probabilidad
    })

# 4. Procesar `estado_metro.csv` (sin coordenadas, asignar manualmente o usar diccionario)
metro_df = pd.read_csv('./Amenazas/estado_metro.csv')
estacion_coords = {
    "San Pablo L1": (-33.4367, -70.7350),
    "Neptuno": (-33.4396, -70.7244),
    "Pajaritos": (-33.4432, -70.7160),
    "Las Rejas": (-33.4565, -70.6970),
    "Ecuador": (-33.4604, -70.6855)
}

for _, row in metro_df.iterrows():
    estacion = row['nombre estacion']
    if estacion in estacion_coords:
        lat, lon = estacion_coords[estacion]
        probabilidad = 1.0 if row['Estado'].lower() == 'cerrado' else 0.2
        probabilidades.append({
            'lat': lat,
            'lon': lon,
            'amenaza': 'Estado del Metro',
            'probabilidad': probabilidad
        })

# Crear un DataFrame final
final_df = pd.DataFrame(probabilidades)

# Guardar como CSV
final_df.to_csv('./pagweb/data/amenazas_probabilidades.csv', index=False)
print("Archivo de probabilidades generado: './pagweb/data/amenazas_probabilidades.csv'")
