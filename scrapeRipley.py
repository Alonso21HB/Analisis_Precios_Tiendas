from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
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

# URL base de la página
base_url = 'https://simple.ripley.com.pe/tecnologia/computacion/laptops?source=search&term=laptop&s=mdco&page='

# Lista para almacenar los datos
data = []

# Número máximo de páginas a recorrer (ajusta según sea necesario)
max_pages = 10

# Iterar sobre cada página
for page in range(1, max_pages + 1):
    # Construir la URL de la página actual
    url = base_url + str(page)
    
    # Abrir la página
    driver.get(url)
    
    # Esperar a que la página cargue completamente
    time.sleep(5)  # Ajusta el tiempo de espera si es necesario
    
    # Encontrar todos los contenedores de productos
    productos = driver.find_elements(By.CLASS_NAME, 'catalog-product-details')
    
    # Iterar sobre cada producto
    for producto in productos:
        try:
            # Extraer el nombre del producto
            nombre = producto.find_element(By.CLASS_NAME, 'catalog-product-details__name').text.strip()
            
            # Extraer la marca
            marca = producto.find_element(By.TAG_NAME, 'span').text.strip()
            
            # Extraer el precio
            precio = producto.find_element(By.CLASS_NAME, 'catalog-prices__offer-price').text.strip()
            
            # Extraer el enlace
            link = producto.find_element(By.XPATH, './ancestor::a').get_attribute('href')
            
            # Agregar los datos a la lista
            data.append([nombre, marca, precio, link])
        except Exception as e:
            # Si hay un error, omitir el producto
            print(f"Error al extraer un producto en la página {page}: {e}")
            continue
    
    print(f"Página {page} procesada. Registros extraídos hasta ahora: {len(data)}")

# Cerrar el navegador
driver.quit()

# Crear un DataFrame con los datos
df = pd.DataFrame(data, columns=['Producto', 'Marca', 'Precio', 'Link'])

# Guardar los datos en un archivo CSV
df.to_csv('productos_ripley.csv', index=False, encoding='utf-8')

print(f"Se han guardado {len(df)} registros en 'productos_ripley.csv'")