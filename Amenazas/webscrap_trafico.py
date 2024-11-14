import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime  # Importamos datetime para manipular la fecha

# URL de la página
url = 'https://www.transporteinforma.cl/'

# Hacer la petición HTTP
response = requests.get(url)

# Verificar si la petición fue exitosa
if response.status_code == 200:
    # Analizar el HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar la sección de "Estado de la movilidad"
    traffic_section = soup.find('section', class_='trafficCondition')

    # Abrir un archivo CSV para escribir la información
    with open('reportes_trafico.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Crear un objeto escritor CSV
        csv_writer = csv.writer(csvfile)
        
        # Escribir el encabezado del CSV
        csv_writer.writerow(['Fecha', 'Hora', 'Descripción', 'Enlace'])
        
        if traffic_section:
            # Buscar los artículos dentro de la lista de condiciones de tráfico
            reports = traffic_section.find_all('a', class_='trafficCondition__list__item')
            
            # Extraer y guardar la información de los reportes
            for report in reports:
                # Dividir el texto del reporte
                partes = report.text.split("-")
                
                # Comprobar si la división contiene al menos tres partes
                if len(partes) >= 3:
                    fecha = partes[0].strip()
                    hora = partes[1].strip()
                    descripcion = partes[2].strip()
                    enlace = report['href']
                    
                    # Convertir la fecha al formato YYYY-MM-DD compatible con PostgreSQL
                    try:
                        # Reemplazamos los puntos medianos por barras para el procesamiento
                        fecha = fecha.replace(" · ", "/")
                        fecha_formateada = datetime.strptime(fecha, '%d/%m/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        fecha_formateada = fecha  # Mantener original si el formato no es compatible
                    
                    # Escribir en el archivo CSV
                    csv_writer.writerow([fecha_formateada, hora, descripcion, enlace])
                else:
                    # Si no se puede dividir, escribe el texto completo y el enlace
                    csv_writer.writerow([report.text.strip(), '', '', report['href']])
        else:
            # Escribir un mensaje en el CSV si no se encontró la sección
            csv_writer.writerow(['Error', 'No se encontró la sección de "Estado de la movilidad".', '', ''])
else:
    with open('reportes_trafico.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Error'])
        csv_writer.writerow([f"Error al acceder a la página: {response.status_code}"])
