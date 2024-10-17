import requests
from bs4 import BeautifulSoup

# URL de la página con el estado del metro
url = 'https://www.metro.cl/el-viaje/estado-red'
response = requests.get(url)

# Ruta al archivo donde guardar la información
output_file = 'estado_metro.txt'

if response.status_code == 200:
    # Crear el objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Abrir el archivo en modo de escritura
    with open(output_file, 'w', encoding='utf-8') as file:
        # Encontrar todos los contenedores de las estaciones usando la clase "col"
        lineas = soup.find_all('div', class_='col')

        # Iterar sobre cada línea y extraer las estaciones
        for linea in lineas:
            # Extraer todas las estaciones (li) dentro de cada línea
            estaciones = linea.find_all('li')

            for estacion in estaciones:
                nombre_estacion = estacion.get_text(strip=True)
                estado = estacion['title']  # El estado está en el atributo 'title'
                # Escribir la información en el archivo
                file.write(f"{nombre_estacion}: {estado}\n")
else:
    # En caso de error, guardar el código de estado en el archivo
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"Error al acceder a la página. Código de estado: {response.status_code}\n")
