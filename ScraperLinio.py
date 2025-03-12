import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL de búsqueda en Linio
URL_BASE = "https://linio.falabella.com.pe/linio-pe/search?Ntt=laptops&page={}"

# Simulación de navegador para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Listas para almacenar los datos
productos, marcas, precios, links = [], [], [], []
paginas_a_recorrer = 5  # Ajusta el número de páginas a recorrer

for i in range(1, paginas_a_recorrer + 1):
    url = URL_BASE.format(i)
    print(f"🔄 Extrayendo datos de: {url}")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al obtener datos de {url}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    elementos = soup.find_all("div", class_="jsx-4014752167")  # Contenedor de producto

    for elem in elementos:
        try:
            marca = elem.find("b", class_="jsx-4014752167 title1 secondary").text.strip()
        except:
            marca = "Desconocida"

        try:
            nombre = elem.find("b", class_="jsx-4014752167 copy2 primary").text.strip()
        except:
            nombre = "Desconocido"

        if "laptop" not in nombre.lower():
            continue  # Ignorar accesorios

        try:
            precio = elem.find("span", class_="copy2 primary high").text.strip()
        except:
            precio = "No disponible"

        try:
            link = elem.find("a")["href"]
            link = f"https://linio.falabella.com.pe{link}"  # Agregar dominio
        except:
            link = "No disponible"

        print(f"✅ Producto encontrado: {nombre} - {marca} - {precio} - {link}")  # Debug

        productos.append(nombre)
        marcas.append(marca)
        precios.append(precio)
        links.append(link)

    time.sleep(2)  # Evitar bloqueos

# Crear DataFrame
df = pd.DataFrame({"Producto": productos, "Marca": marcas, "Precio": precios, "Link": links})
df.drop_duplicates(inplace=True)  # Eliminar duplicados
df.to_csv("linio_laptops_corregido.csv", index=False)

print(f"✅ Scraping finalizado. Se guardaron {len(df)} registros en 'linio_laptops_corregido.csv'.")



