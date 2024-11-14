import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import csv
import concurrent.futures

# Crear una sesión de requests para mejorar el rendimiento
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'})

def esta_permitido_por_robots(url):
    """
    Verifica si la URL está permitida según las reglas del robots.txt proporcionadas.
    """
    if re.search(r'/alt-|/aux-', url):
        return False
    return True

def extraer_informacion(url):
    """
    Extrae información específica de la página, como el contenido del div con id 'ficha_informacion' 
    y 'article_i__alt2021_arMuseo_Titulo_1'.
    """
    try:
        # Hacemos una solicitud GET a la URL
        respuesta = session.get(url)
        if respuesta.status_code != 200:
            return None
        
        # Parseamos el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Extraemos el div con id 'ficha_informacion'
        ficha = soup.find('div', id='ficha_informacion')
        contenido_ficha = ficha.get_text(strip=True) if ficha else None
        
        # Extraemos el div con id 'article_i__alt2021_arMuseo_Titulo_1'
        articulo = soup.find('div', id='article_i__alt2021_arMuseo_Titulo_1')
        contenido_articulo = articulo.get_text(strip=True) if articulo else None
        
        # Creamos un diccionario con la información extraída
        info = {
            'url': url,
            'ficha_informacion': contenido_ficha,
            'article_i__alt2021_arMuseo_Titulo_1': contenido_articulo
        }
        
        # Solo devolvemos la información si al menos uno de los div tiene contenido
        if contenido_ficha or contenido_articulo:
            return info
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error al extraer información de {url}: {e}")
        return None

def obtener_enlaces(url, dominio_base):
    """
    Esta función toma una URL y devuelve todos los enlaces encontrados en esa página
    que pertenecen al mismo dominio base y que están permitidos según las reglas del robots.txt.
    """
    try:
        # Hacemos una solicitud GET a la URL
        respuesta = session.get(url)
        if respuesta.status_code != 200:
            return []
        
        # Parseamos el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Obtenemos todos los enlaces <a> con un atributo href
        enlaces = set()
        for link in soup.find_all('a', href=True):
            # Convertimos enlaces relativos en absolutos
            enlace_absoluto = urljoin(url, link['href'])  
            
            # Comprobamos que el enlace pertenece al mismo dominio
            if urlparse(enlace_absoluto).netloc == dominio_base:
                # Verificamos si el enlace cumple con las restricciones de robots.txt
                if esta_permitido_por_robots(enlace_absoluto):
                    enlaces.add(enlace_absoluto)
                else:
                    print(f"El enlace {enlace_absoluto} está bloqueado por robots.txt")
                
        return list(enlaces)
    
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud a {url}: {e}")
        return []

def scrape_dominio_interno(url_inicial, profundidad=1):
    dominio_base = urlparse(url_inicial).netloc
    visitados = set()  # URLs ya visitadas
    pendientes = {url_inicial}  # URLs pendientes de visitar
    informacion_extraida = []  # Almacenar la información extraída de cada página

    for nivel in range(profundidad):
        nuevos_pendientes = set()
        print(f"\nProfundidad {nivel + 1}")

        # Procesar URLs en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(extraer_informacion, url): url for url in pendientes}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                if url not in visitados:
                    visitados.add(url)
                    try:
                        info = future.result()
                        if info:
                            informacion_extraida.append(info)
                        
                        enlaces = obtener_enlaces(url, dominio_base)
                        nuevos_pendientes.update(enlaces)
                    except Exception as e:
                        print(f"Error en la URL {url}: {e}")

        pendientes = nuevos_pendientes

    return informacion_extraida

def guardar_informacion_en_archivo(informacion, nombre_archivo):
    """
    Guarda la información extraída en un archivo CSV y la muestra en la consola,
    solo si se ha encontrado contenido en alguno de los divs.
    """
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        # Crear el objeto escritor CSV
        csv_writer = csv.writer(archivo_csv)
        
        # Escribir el encabezado del CSV
        csv_writer.writerow(['URL', 'Ficha Información', 'Article Título'])

        for pagina in informacion:
            # Solo guardamos información si al menos un div tiene contenido
            if pagina['ficha_informacion'] or pagina['article_i__alt2021_arMuseo_Titulo_1']:
                # Escribir la fila en el CSV
                csv_writer.writerow([
                    pagina['url'], 
                    pagina['ficha_informacion'] if pagina['ficha_informacion'] else '', 
                    pagina['article_i__alt2021_arMuseo_Titulo_1'] if pagina['article_i__alt2021_arMuseo_Titulo_1'] else ''
                ])
                
                # Mostrar información en la consola
                print(f"\nURL: {pagina['url']}")
                print("="*80)
                print("Información del div 'article_i__alt2021_arMuseo_Titulo_1':")
                print(pagina['article_i__alt2021_arMuseo_Titulo_1'])
                print("\nInformación del div 'ficha_informacion':")
                print(pagina['ficha_informacion'])
                print("\n" + "="*80 + "\n")

# URL de inicio para el scraping
url_inicial = "https://www.registromuseoschile.cl/663/w3-channel.html"  # Reemplazar con la URL deseada
informacion = scrape_dominio_interno(url_inicial, profundidad=3)  # Profundidad para seguir enlaces

# Guardamos la información extraída en un archivo CSV
nombre_archivo = "informacion_extraida.csv"
guardar_informacion_en_archivo(informacion, nombre_archivo)
