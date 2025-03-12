import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL base de búsqueda en Linio
URL_BASE = "https://linio.falabella.com.pe/linio-pe/search?Ntt=laptops&page={}"

# Simulación de un navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Número de productos deseados
productos_totales = 300  # Para asegurarnos de tener más de 200 registros
productos_por_pagina = 48  # Linio muestra aprox. 48 productos por página
paginas_a_recorrer = (productos_totales // productos_por_pagina) + 1

# Listas para almacenar los datos
productos = []
marcas = []
precios = []
links = []

# Recorrer las páginas
for i in range(1, paginas_a_recorrer + 1):
    url = URL_BASE.format(i)
    print(f"🔄 Extrayendo datos de: {url}")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        elementos = soup.find_all("div", class_="jsx-4014752167")  # Bloques de productos

        for elem in elementos:
            try:
                marca = elem.find("b", class_="jsx-4014752167 title1 secondary jsx-3451706699 bold pod-title title-rebrand").text.strip()
            except:
                marca = "No disponible"

            try:
                nombre = elem.find("b", class_="jsx-4014752167 copy2 primary jsx-3451706699 normal line-clamp line-clamp-3 pod-subTitle subTitle-rebrand").text.strip()
            except:
                nombre = "No disponible"

            try:
                precio = elem.find("span", class_="copy2 primary high jsx-4014752167").text.strip()
            except:
                precio = "No disponible"

            try:
                link = elem.find("a")["href"]
                link = f"https://linio.falabella.com.pe{link}"  # Agregar dominio base
            except:
                link = "No disponible"

            productos.append(nombre)
            marcas.append(marca)
            precios.append(precio)
            links.append(link)

        # Evitar bloqueos con una pausa entre solicitudes
        time.sleep(2)

    else:
        print(f"❌ Error al obtener datos de {url}: {response.status_code}")
        break

# Ajustar listas si tienen diferente tamaño
min_length = min(len(productos), len(marcas), len(precios), len(links))
productos = productos[:min_length]
marcas = marcas[:min_length]
precios = precios[:min_length]
links = links[:min_length]

# Guardar en CSV
df = pd.DataFrame(zip(productos, marcas, precios, links), columns=["Producto", "Marca", "Precio", "Link"])
df.to_csv("linio_laptops.csv", index=False)

print(f"✅ Scraping finalizado. Datos guardados en 'linio_laptops.csv' con {len(df)} registros.")

