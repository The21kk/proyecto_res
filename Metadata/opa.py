import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('museos_Scraping.csv')

# Reemplazar NaN con 0 en la columna 'Museum Reviews' y eliminar puntos, luego convertir a enteros
df['Museum Reviews'] = df['Museum Reviews'].fillna(0).astype(str).str.replace('.', '', regex=False).astype(int)

# Guardar el archivo CSV modificado
df.to_csv('museos_Scraping.csv', index=False)

print("Archivo modificado guardado como 'museos_Scraping_modificado.csv'")
