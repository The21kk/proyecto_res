import requests
from bs4 import BeautifulSoup

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

    if traffic_section:
        # Buscar los artículos dentro de la lista de condiciones de tráfico
        reports = traffic_section.find_all('a', class_='trafficCondition__list__item')
        
        # Extraer y mostrar la información de los reportes
        for report in reports:
            # Dividir el texto del reporte
            partes = report.text.split(" - ")
            
            # Comprobar si la división contiene al menos tres partes
            if len(partes) >= 3:
                fecha = partes[0].strip()
                hora = partes[1].strip()
                descripcion = partes[2].strip()
                enlace = report['href']
                
                print(f"Fecha: {fecha}")
                print(f"Hora: {hora}")
                print(f"Descripción: {descripcion}")
                print(f"Enlace: {enlace}\n")
            else:
                print(report.text)
    else:
        print("No se encontró la sección de 'Estado de la movilidad'.")
else:
    print(f"Error al acceder a la página: {response.status_code}")
