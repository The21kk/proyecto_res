import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re  # Importar la biblioteca re para expresiones regulares

# User-Agent para prevenir el bloqueo por parte de TripAdvisor
user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/90.0.4430.212 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# Configuración del proxy
proxies = {
    "https": "scraperapi.session_number=20:826766cf66349f43e3efa4cbcc38d38e@proxy-server.scraperapi.com:8001"
}

# Función para obtener el contenido de la página
def get_page_contents(url):
    page = requests.get(url, headers=user_agent, proxies=proxies, verify=False)
    return BeautifulSoup(page.text, 'html.parser')

# Función para extraer los nombres, ratings y reviews de los museos
def get_museums_ratings_reviews_from_page(soup):
    museums = []
    ratings = []
    reviews = []
    
    # Obtener nombres de los museos
    for name in soup.findAll('div', {'class': 'XfVdV o AIbhI'}):
        cleaned_name = re.sub(r'^\d+\.\s*', '', name.text.strip())
        museums.append(cleaned_name)

    # Obtener ratings de los museos
    for rating_div in soup.find_all('div', class_='jVDab W f u w JqMhy'):
        rating_svg = rating_div.find('svg', class_='UctUV d H0 hzzSG')
        if rating_svg:
            ratings.append(rating_svg.text.strip())
        else:
            ratings.append("Sin valoración")  # Cambiar a "Sin valoración"
    
    # Obtener número de reviews de los museos
    for review_span in soup.find_all('span', class_='biGQs _P pZUbB osNWb'):
        if review_span:
            reviews.append(review_span.text.strip())
        else:
            reviews.append("Sin reviews")  # Si no hay número de reviews, marcarlo como "Sin reviews"
    
    # Asegurarse de que las listas tengan la misma longitud
    while len(ratings) < len(museums):
        ratings.append("Sin valoración")
    
    while len(reviews) < len(museums):
        reviews.append("Sin reviews")
    
    return museums, ratings, reviews

# URLs base para alternar entre los dominios .cl y .es
base_url_cl = 'https://www.tripadvisor.cl/Attractions-g294291-Activities-c49-oa{}-Chile.html'
base_url_es = 'https://www.tripadvisor.es/Attractions-g294291-Activities-c49-oa{}-Chile.html'

# URL de la primera página
first_page_url = 'https://www.tripadvisor.cl/Attractions-g294291-Activities-c49-Chile.html'

# Número de páginas a scrape
num_pages = 11
museums_all_pages = []
ratings_all_pages = []
reviews_all_pages = []
max_retries = 3  # Número máximo de intentos antes de pasar a la siguiente página

# Scraping de la primera página con reintentos
retry_attempts = 0
while retry_attempts < max_retries:
    print(f"Scraping first page: {first_page_url}")
    soup = get_page_contents(first_page_url)
    time.sleep(10)
    museums_on_first_page, ratings_on_first_page, reviews_on_first_page = get_museums_ratings_reviews_from_page(soup)
    
    if museums_on_first_page:  # Si se encuentran museos, agregar los datos y salir del bucle
        museums_all_pages.extend(museums_on_first_page)
        ratings_all_pages.extend(ratings_on_first_page)
        reviews_all_pages.extend(reviews_on_first_page)
        print(f"Museums found on first page: {len(museums_on_first_page)}")
        break
    else:
        retry_attempts += 1
        print(f"No museums found on first page, retrying ({retry_attempts}/{max_retries})...")
        time.sleep(10)  # Espera antes de volver a intentar
        
if retry_attempts == max_retries:
    print("Max retries reached for the first page, moving to next page.")

# Scraping de las páginas siguientes
for i in range(30, num_pages * 30, 30):
    retry_attempts = 0
    while retry_attempts < max_retries:
        # Alternar entre dominios .cl y .es
        if (i // 30) % 2 == 0:
            url = base_url_cl.format(i)
        else:
            url = base_url_es.format(i)
        
        print(f"Scraping page: {url}")
        
        soup = get_page_contents(url)
        time.sleep(10)
        museums_on_page, ratings_on_page, reviews_on_page = get_museums_ratings_reviews_from_page(soup)
        
        if museums_on_page:  # Si se encuentran museos, agregar los datos y continuar
            museums_all_pages.extend(museums_on_page)
            ratings_all_pages.extend(ratings_on_page)
            reviews_all_pages.extend(reviews_on_page)
            print(f"Museums found on page {i // 30 + 1}: {len(museums_on_page)}")
            break
        else:
            retry_attempts += 1
            print(f"No museums found on page {i // 30 + 1}, retrying ({retry_attempts}/{max_retries})...")
            time.sleep(10)  # Espera antes de volver a intentar
            
    if retry_attempts == max_retries:
        print(f"Max retries reached for page {i // 30 + 1}, moving to next page.")

# Crear el diccionario con los nombres, ratings y reviews
data = {'Museum Names': museums_all_pages, 'Museum Ratings': ratings_all_pages, 'Museum Reviews': reviews_all_pages}

# Crear el dataframe
museums_df = pd.DataFrame.from_dict(data)

# Mostrar las primeras filas
print("First 10 museums scraped:")
print(museums_df.head(10))

# Convertir el dataframe en archivo CSV
museums_df.to_csv('museos_Scraping.csv', index=False, header=True)

print(f"Total museums scraped: {len(museums_all_pages)}")