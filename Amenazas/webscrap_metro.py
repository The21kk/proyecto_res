import requests
from bs4 import BeautifulSoup
import csv

# URL de la página con el estado del metro
url = 'https://www.metro.cl/el-viaje/estado-red'
response = requests.get(url)

# Ruta al archivo donde guardar la información
output_file = 'estado_metro.csv'

if response.status_code == 200:
    # Crear el objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Abrir el archivo CSV en modo de escritura
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Crear un objeto escritor CSV
        csv_writer = csv.writer(csvfile)
        
        # Escribir el encabezado del CSV
        csv_writer.writerow(['Nombre Estación', 'Estado'])
        
        # Encontrar todos los contenedores de las estaciones usando la clase "col"
        lineas = soup.find_all('div', class_='col')

        # Iterar sobre cada línea y extraer las estaciones
        for linea in lineas:
            # Extraer todas las estaciones (li) dentro de cada línea
            estaciones = linea.find_all('li')

            for estacion in estaciones:
                nombre_estacion = estacion.get_text(strip=True)
                estado = estacion['title']  # El estado está en el atributo 'title'
                
                # Escribir la información en el archivo CSV
                csv_writer.writerow([nombre_estacion, estado])
else:
    # En caso de error, guardar el código de estado en el archivo CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Error'])
        csv_writer.writerow([f"Error al acceder a la página. Código de estado: {response.status_code}"])
