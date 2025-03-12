import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Simulación de navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Parámetros de configuración
productos_totales = 200  # Número de productos deseados
productos_por_pagina = 50  # Mercado Libre muestra aprox. 50 por página
paginas_a_recorrer = (productos_totales // productos_por_pagina) + 1

# Listas para almacenar datos
productos = []
marcas = []
precios = []
links = []

# Recorrer las páginas
for i in range(paginas_a_recorrer):
    offset = i * productos_por_pagina + 1
    url = f"https://listado.mercadolibre.com.pe/laptops_Desde_{offset}"
    
    print(f"🔄 Extrayendo datos de: {url}")
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        elementos = soup.find_all("div", class_="poly-card__content")

        for elem in elementos:
            try:
                marca = elem.find("span", class_="poly-component__brand").text.strip()
            except:
                marca = "No disponible"

            try:
                nombre = elem.find("a", class_="poly-component__title").text.strip()
            except:
                nombre = "No disponible"

            try:
                link = elem.find("a", class_="poly-component__title")["href"]
            except:
                link = "No disponible"

            productos.append(nombre)
            marcas.append(marca)
            links.append(link)

        # Extraer precios
        precios_elementos = soup.find_all("span", class_="andes-money-amount__fraction")

        for precio_elem in precios_elementos:
            try:
                precio = precio_elem.text.strip()
            except:
                precio = "No disponible"
            precios.append(precio)

        # Evitar hacer demasiadas solicitudes en poco tiempo
        time.sleep(2)  # Esperar 2 segundos entre páginas

    else:
        print(f"❌ Error al obtener datos de {url}: {response.status_code}")
        break  # Si hay un error, detener el scraping

# Ajustar listas si no tienen la misma cantidad de elementos
min_length = min(len(productos), len(marcas), len(precios), len(links))
productos = productos[:min_length]
marcas = marcas[:min_length]
precios = precios[:min_length]
links = links[:min_length]

# Guardar en CSV
df = pd.DataFrame(zip(productos, marcas, precios, links), columns=["Producto", "Marca", "Precio", "Link"])
df.to_csv("mercadolibre_laptops.csv", index=False)

print(f"✅ Scraping finalizado. Datos guardados en 'mercadolibre_laptops.csv' con {len(df)} registros.")

