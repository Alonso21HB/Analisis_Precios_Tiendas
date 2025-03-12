import requests
from bs4 import BeautifulSoup
import csv

# URL de la página a scrapear
url = "https://cyccomputer.pe/categoria/338-laptop-intel"

# Encabezados para evitar bloqueo
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Realizar la solicitud
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Lista para almacenar los datos
laptops = []

# Extraer cada producto
for item in soup.find_all("h2", class_="productName"):
    product_name = item.text.strip()
    product_link = item.find("a")["href"] if item.find("a") else "No disponible"
    
    # Buscar la marca
    brand_tag = item.find_next("div", class_="manufacturer_name")
    brand = brand_tag.text.strip().replace("Marca:", "").strip() if brand_tag else "No disponible"
    
    # Buscar el precio en soles
    price_tag = item.find_next("span", class_="price")
    price_text = price_tag.text.strip() if price_tag else "No disponible"
    
    # Limpiar el precio y obtener solo la versión en soles
    price_soles = price_text.split("(S/")[-1].replace(")", "").strip() if "S/" in price_text else "No disponible"
    
    # Agregar a la lista
    laptops.append([product_name, brand, price_soles, product_link])

# Guardar en CSV
csv_filename = "laptops_cyc_computer.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Producto", "Marca", "Precio (S/)", "Link"])
    writer.writerows(laptops)

print(f"Se han guardado {len(laptops)} laptops en {csv_filename}")
