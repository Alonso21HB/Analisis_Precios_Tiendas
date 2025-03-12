import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurar Selenium con ChromeDriver
options = Options()
options.add_argument("--headless")  # Ejecutar sin abrir el navegador
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--no-sandbox")

# Inicializar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de la página
url = "https://hiraoka.com.pe/computo-y-tecnologia/computadoras/laptops"
driver.get(url)

# Esperar a que se cargue la página
time.sleep(5)

# Hacer scroll para cargar más productos
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Esperar que carguen más productos
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break  # Salir cuando ya no se cargan más productos
    last_height = new_height

# Obtener los productos
productos = driver.find_elements(By.CLASS_NAME, "product-item")

# Lista para almacenar datos
data = []

for producto in productos:
    try:
        # Extraer nombre del producto
        nombre_tag = producto.find_element(By.CLASS_NAME, "product-item-name")
        nombre = nombre_tag.text.strip() if nombre_tag else "No disponible"

        # Extraer marca
        marca_tag = producto.find_element(By.CLASS_NAME, "product-item-brand")
        marca = marca_tag.text.strip() if marca_tag else "No disponible"

        # Extraer precio
        precio_tag = producto.find_element(By.CLASS_NAME, "price")
        precio = precio_tag.text.strip() if precio_tag else "No disponible"

        # Extraer enlace
        link_tag = producto.find_element(By.CLASS_NAME, "product-item-link")
        link = link_tag.get_attribute("href") if link_tag else "No disponible"

        # Agregar a la lista
        data.append([nombre, marca, precio, link])

    except Exception as e:
        print(f"Error en un producto: {e}")

# Cerrar navegador
driver.quit()

# Guardar en CSV
df = pd.DataFrame(data, columns=["Producto", "Marca", "Precio", "Link"])
df.to_csv("hiraoka_laptops.csv", index=False, encoding="utf-8")

print(f"✅ Datos guardados en 'hiraoka_laptops.csv' con {len(data)} registros.")

