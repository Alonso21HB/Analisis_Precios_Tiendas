import requests
import pandas as pd
from bs4 import BeautifulSoup

# Base URL
base_url = "https://hiraoka.com.pe/computo-y-tecnologia/computadoras/laptops?p={}"

# Headers para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Listas para almacenar datos
productos = []
marcas = []
precios = []
links = []

# Recorremos varias páginas (ajusta el rango según el número de páginas disponibles)
for pagina in range(1, 10):  # Ajusta el rango según la cantidad de páginas en la web
    url = base_url.format(pagina)
    print(f"Scrapeando página {pagina}...")

    # Hacer la solicitud HTTP
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar todos los productos en la página
        items = soup.find_all("div", class_="product-item-details")

        for item in items:
            # Obtener la marca
            marca_tag = item.find("strong", class_="product brand product-item-brand")
            marca = marca_tag.text.strip() if marca_tag else "Sin marca"

            # Obtener el nombre del producto desde 'title'
            producto_tag = item.find("strong", class_="product name product-item-name")
            producto = producto_tag.text.strip() if producto_tag else "Sin nombre"

            # Obtener el precio
            precio_tag = item.find("span", class_="price")
            precio = precio_tag.text.strip() if precio_tag else "Sin precio"

            # Obtener el enlace del producto
            link_tag = item.find("a", class_="product-item-link")
            link = link_tag["href"] if link_tag and link_tag.has_attr("href") else "Sin link"

            # Asegurar que el link tenga la URL completa
            link = f"https://hiraoka.com.pe{link}" if "http" not in link else link

            # Guardar en listas
            productos.append(producto)
            marcas.append(marca)
            precios.append(precio)
            links.append(link)

    else:
        print(f"❌ No se pudo acceder a la página {pagina}, código: {response.status_code}")
        break  # Detenemos la ejecución si hay error en una página

# Crear DataFrame
df = pd.DataFrame({
    "Producto": productos,
    "Marca": marcas,
    "Precio": precios,
    "Link": links
})

# Guardar en CSV
df.to_csv("laptops_hiraoka.csv", index=False, encoding="utf-8-sig")
print(f"✅ Archivo 'laptops_hiraoka.csv' guardado con {len(df)} registros.")


