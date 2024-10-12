import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

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
        respuesta = requests.get(url)
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
        respuesta = requests.get(url)
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

def formatear_informacion(contenido):
    """
    Formatea el texto extraído para hacerlo más legible, agregando saltos de línea y 
    separando adecuadamente las palabras clave.
    """
    # Insertar saltos de línea donde sea apropiado
    contenido = re.sub(r'(\w)([A-Z])', r'\1\n\2', contenido)  # Separar palabras juntas
    contenido = contenido.replace('Dirección', '\nDirección: ')
    contenido = contenido.replace('Región', '\nRegión: ')
    contenido = contenido.replace('Horario de visita', '\nHorario de visita: ')
    contenido = contenido.replace('Valor entrada', '\nValor entrada: ')
    contenido = contenido.replace('Fechas de cierre', '\nFechas de cierre: ')
    contenido = contenido.replace('Contactar', '\nContactar: ')
    contenido = contenido.replace('Teléfono', '\nTeléfono: ')
    contenido = contenido.replace('Correo electrónico', '\nCorreo electrónico: ')
    contenido = contenido.replace('Director(a)', '\nDirector(a) o encargado(a): ')
    contenido = contenido.replace('Seguir e interactuar', '\nSeguir e interactuar: ')
    contenido = contenido.replace('Otro recurso tecnológico', '\nOtro recurso tecnológico: ')
    
    return contenido

def scrape_dominio_interno_test(url_inicial, profundidad=1, max_urls_por_profundidad=10):
    """
    Esta función realiza scraping limitado para testeo, visitando hasta un máximo de 10 URLs por nivel de profundidad.
    """
    dominio_base = urlparse(url_inicial).netloc
    
    visitados = set()  # URLs ya visitadas
    pendientes = {url_inicial}  # URLs pendientes de visitar
    
    informacion_extraida = []  # Almacenar la información extraída de cada página

    for nivel in range(profundidad):
        nuevos_pendientes = set()
        print(f"\nProfundidad {nivel + 1}")
        url_count = 0
        while pendientes and url_count < max_urls_por_profundidad:
            url = pendientes.pop()
            if url not in visitados:
                print(f"Visitando: {url}")
                visitados.add(url)
                
                # Extraemos la información de la página
                info = extraer_informacion(url)
                if info:
                    informacion_extraida.append(info)  # Guardamos la información extraída si se encuentra
                
                # Obtenemos los enlaces dentro del mismo dominio
                enlaces = obtener_enlaces(url, dominio_base)
                nuevos_pendientes.update(enlaces)  # Añadimos nuevos enlaces para procesar
                
                # Incrementamos el contador de URLs visitadas
                url_count += 1
            
            time.sleep(1)  # Retraso para no sobrecargar el servidor
        
        # Actualizamos los pendientes para el siguiente nivel de profundidad
        pendientes = nuevos_pendientes

    return informacion_extraida

def guardar_informacion_en_archivo(informacion, nombre_archivo):
    """
    Guarda la información extraída en un archivo de texto y la muestra en la consola,
    solo si se ha encontrado contenido en alguno de los divs, y formatea el contenido para mejor legibilidad.
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        for pagina in informacion:
            # Solo guardamos información si al menos un div tiene contenido
            if pagina['ficha_informacion'] or pagina['article_i__alt2021_arMuseo_Titulo_1']:
                archivo.write(f"URL: {pagina['url']}\n")
                archivo.write("="*80 + "\n")
                
                # Primero mostramos la información del div 'article_i__alt2021_arMuseo_Titulo_1'
                if pagina['article_i__alt2021_arMuseo_Titulo_1']:
                    archivo.write("Información del div 'article_i__alt2021_arMuseo_Titulo_1':\n")
                    contenido_formateado = formatear_informacion(pagina['article_i__alt2021_arMuseo_Titulo_1'])
                    archivo.write(f"{contenido_formateado}\n")
                
                archivo.write("\n")
                
                # Luego mostramos la información del div 'ficha_informacion'
                if pagina['ficha_informacion']:
                    archivo.write("Información del div 'ficha_informacion':\n")
                    contenido_formateado = formatear_informacion(pagina['ficha_informacion'])
                    archivo.write(f"{contenido_formateado}\n")
                
                archivo.write("\n" + "="*80 + "\n")
    
    # Mostramos la información extraída también en la consola
    for pagina in informacion:
        if pagina['ficha_informacion'] or pagina['article_i__alt2021_arMuseo_Titulo_1']:
            print(f"\nURL: {pagina['url']}")
            print("="*80)
            
            # Primero la información del div 'article_i__alt2021_arMuseo_Titulo_1'
            if pagina['article_i__alt2021_arMuseo_Titulo_1']:
                print("Información del div 'article_i__alt2021_arMuseo_Titulo_1':")
                contenido_formateado = formatear_informacion(pagina['article_i__alt2021_arMuseo_Titulo_1'])
                print(contenido_formateado)
            
            print("\n")
            
            # Luego la información del div 'ficha_informacion'
            if pagina['ficha_informacion']:
                print("Información del div 'ficha_informacion':")
                contenido_formateado = formatear_informacion(pagina['ficha_informacion'])
                print(contenido_formateado)
            
            print("\n" + "="*80 + "\n")

# URL de inicio para el scraping
url_inicial = "https://www.registromuseoschile.cl/663/w3-channel.html"  # Reemplazar con la URL deseada
informacion = scrape_dominio_interno_test(url_inicial, profundidad=3, max_urls_por_profundidad=10)  # Profundidad para seguir enlaces

# Guardamos la información extraída en un archivo de texto
nombre_archivo = "informacion_extraida_test.txt"
guardar_informacion_en_archivo(informacion, nombre_archivo)

# Mostramos la información extraída de cada página
for pagina in informacion:
    if pagina['ficha_informacion'] or pagina['article_i__alt2021_arMuseo_Titulo_1']:
        print(f"\nInformación extraída de {pagina['url']}:")
        print(f"Contenido del div 'article_i__alt2021_arMuseo_Titulo_1': {formatear_informacion(pagina['article_i__alt2021_arMuseo_Titulo_1'])}")
        print(f"Contenido del div 'ficha_informacion': {formatear_informacion(pagina['ficha_informacion'])}")

