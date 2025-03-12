from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configurar las opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo sin cabeza (sin interfaz gráfica)
chrome_options.add_argument("--disable-gpu")  # Desactivar GPU para evitar problemas
chrome_options.add_argument("--window-size=1920,1080")  # Tamaño de la ventana
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Simular un navegador real

# Usar WebDriver Manager para manejar ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL de la página
url = 'https://www.pcfactory.com.pe/producto/busqueda_avanzada?query=laptops'

# Abrir la página
driver.get(url)

# Esperar a que la página cargue completamente
time.sleep(10)  # Aumenta el tiempo de espera para asegurar que los productos se carguen

# Encontrar todos los contenedores de productos
try:
    wait = WebDriverWait(driver, 10)
    productos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product')))  # Ajusta la clase según la estructura real
except Exception as e:
    print(f"Error al encontrar los productos: {e}")
    driver.quit()
    exit()

# Lista para almacenar los datos
data = []

# Iterar sobre cada producto
for producto in productos:
    try:
        # Extraer el nombre del producto
        nombre = producto.find_element(By.CLASS_NAME, 'product__card-title').text.strip()
    except:
        nombre = "No disponible"
    
    try:
        # Extraer la marca
        marca = producto.find_element(By.CLASS_NAME, 'product__main-title').text.strip()
    except:
        marca = "No disponible"
    
    try:
        # Extraer el precio (sin el porcentaje)
        precio_contenedor = producto.find_element(By.CLASS_NAME, 'alineado-porcentaje-precio')
        precio_texto = precio_contenedor.text.strip()
        
        # Separar el precio del porcentaje
        precio = precio_texto.split()[-1]  # Obtiene el último elemento (el precio)
    except:
        precio = "No disponible"
    
    try:
        # Extraer el enlace
        link = producto.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        link = "No disponible"
    
    # Agregar los datos a la lista
    data.append([nombre, marca, precio, link])

# Cerrar el navegador
driver.quit()

# Crear un DataFrame con los datos
df = pd.DataFrame(data, columns=['Producto', 'Marca', 'Precio', 'Link'])

# Guardar los datos en un archivo CSV
df.to_csv('productos_pcfactory.csv', index=False, encoding='utf-8')

print(f"Se han guardado {len(df)} registros en 'productos_pcfactory.csv'")