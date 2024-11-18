import geopandas as gpd
import pandas as pd
from scipy.spatial import distance_matrix
import numpy as np

# Rutas a los archivos
ruta_geojson = './data/capa1.geojson'
ruta_robos = '/home/nicolas/Desktop/U/proyecto_res/Amenazas/robos.csv'
ruta_trafico = '/home/nicolas/Desktop/U/proyecto_res/Amenazas/reportes_trafico.csv'
ruta_feriados = '/home/nicolas/Desktop/U/proyecto_res/Amenazas/feriados_chile2024.csv'
ruta_estado_metro = '/home/nicolas/Desktop/U/proyecto_res/Amenazas/estado_metro.csv'

# Cargar datos de museos
museos_gdf = gpd.read_file(ruta_geojson)
museos_gdf['lat'] = museos_gdf.geometry.y
museos_gdf['lon'] = museos_gdf.geometry.x
museos_df = museos_gdf[['nombre', 'lat', 'lon']].rename(columns={'nombre': 'nodo_id'})

# Cargar datos de amenazas
robos_df = pd.read_csv(ruta_robos)
trafico_df = pd.read_csv(ruta_trafico)
feriados_df = pd.read_csv(ruta_feriados)
estado_metro_df = pd.read_csv(ruta_estado_metro)

# Añadir columnas necesarias a los datos
robos_df['prob_robos'] = robos_df['Robos'] / robos_df['Robos'].max()

trafico_df['prob_trafico'] = trafico_df['Descripción'].apply(
    lambda desc: 0.8 if "suspendido" in desc.lower() else 0.5 if "reducción de pistas" in desc.lower() else 0.2
)

feriados_df['prob_feriado'] = feriados_df['irrenunciable'].apply(lambda x: 0.5 if x == 1 else 0.2)

estado_metro_df['prob_metro'] = estado_metro_df['Estado'].apply(
    lambda estado: 0.7 if "cerrada" in estado.lower() else 0.5 if "interrupción parcial" in estado.lower() else 0.1
)

def calcular_probabilidades_museos(museos_df, robos_df, feriados_df):
    coords_nodos = museos_df[['lat', 'lon']].to_numpy()
    nodos_ids = museos_df['nodo_id'].tolist()

    # Robos: Reducir impacto escalando las contribuciones
    coords_robos = robos_df[['Lat', 'Lon']].to_numpy()
    probs_robos = 0.2 * (robos_df['Robos'] / robos_df['Robos'].max()).to_numpy()  # Convertir a numpy array
    dist_nodos_robos = distance_matrix(coords_nodos, coords_robos)
    prob_robos_nodos = (dist_nodos_robos <= 500) * probs_robos.reshape(1, -1)  # Asegurar dimensiones compatibles

    # Feriados: Reducir impacto
    prob_feriados = feriados_df['prob_feriado'].mean() * 0.05  # Escalar contribución de feriados

    # Sumar contribuciones con pesos reducidos
    prob_fallos_nodos = (
        0.3 * prob_robos_nodos.sum(axis=1) +  # Peso reducido para robos
        prob_feriados                         # Peso muy reducido para feriados
    )
    prob_fallos_nodos = np.clip(prob_fallos_nodos, 0, 1)  # Limitar a 1.0

    return pd.DataFrame({
        'nodo_id': nodos_ids,
        'lat': coords_nodos[:, 0],
        'lon': coords_nodos[:, 1],
        'probabilidad_fallo': prob_fallos_nodos
    })




# Calcular probabilidades de fallo
nodos_final_df = calcular_probabilidades_museos(museos_df, robos_df, feriados_df)

# Guardar resultados
nodos_final_df.to_csv('/home/nicolas/Desktop/U/proyecto_res/nodos_museos_probabilidades.csv', index=False)
print(nodos_final_df.head())
