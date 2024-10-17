import requests
import pandas as pd

# URL de la API de feriados en Chile
url = "https://apis.digital.gob.cl/fl/feriados/2024"

# Definir un encabezado User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

# Intentar realizar la solicitud con el encabezado User-Agent
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanzar un error para códigos de respuesta 4xx o 5xx

    # Procesar los datos si la solicitud fue exitosa
    data = response.json()

    # Crear una lista para almacenar los datos procesados
    feriados_list = []

    # Procesar cada feriado y extraer la información necesaria
    for feriado in data:
        feriado_info = {
            "nombre": feriado["nombre"],
            "fecha": feriado["fecha"],
            "irrenunciable": feriado["irrenunciable"],
            "tipo": feriado["tipo"],
            "leyes": ", ".join([f"{ley['nombre']} ({ley['url']})" for ley in feriado.get("leyes", [])])
        }
        feriados_list.append(feriado_info)

    # Crear un DataFrame a partir de la lista de feriados
    feriados_df = pd.DataFrame(feriados_list)

    # Guardar el DataFrame en un archivo CSV
    feriados_df.to_csv('feriados_chile2024.csv', index=False)
    print("Los datos han sido guardados en 'feriados_chile2024.csv'.")

except requests.exceptions.RequestException as e:
    print(f"Error al intentar obtener datos: {e}")
