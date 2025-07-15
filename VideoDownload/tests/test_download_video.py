import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.pdf_report import generar_reporte

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")  # Ajusta si descargas a otra carpeta
pasos = []
success = False

def esperar_acceso_archivo(path, timeout=20):
    for _ in range(timeout):
        try:
            with open(path, "rb"):
                return True
        except (PermissionError, FileNotFoundError):
            time.sleep(1)
    return False

# 1. Configurar navegador para descargas automáticas
options = Options()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 10)

try:
    print("[1] Abriendo página principal...")
    driver.get("http://localhost:3000")
    pasos.append("Página principal abierta")

    print("[2] Haciendo clic en 'Explorar'...")
    explorar = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Explorar")))
    explorar.click()
    pasos.append("Se hizo clic en 'Explorar'")

    time.sleep(2)  # Espera a que el grid cargue

    print("[3] Seleccionando primer video del grid...")
    thumbnails = driver.find_elements(By.CLASS_NAME, "video-card-wrapper")
    if not thumbnails:
        raise Exception("No hay videos disponibles en el grid")
    thumbnails[0].click()
    pasos.append("Primer video abierto desde el grid")

    print("[4] Haciendo clic en el botón de descarga...")
    boton_descarga = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Descargar video")))
    filename = boton_descarga.get_attribute("download")
    boton_descarga.click()
    pasos.append("Botón de descarga presionado")

    expected_path = os.path.join(DOWNLOAD_DIR, filename)
    print(f"[5] Esperando que se descargue: {expected_path}")

    if esperar_acceso_archivo(expected_path, timeout=30):
        pasos.append(f"El archivo fue descargado correctamente: {filename}")
        success = True
    else:
        pasos.append("El archivo no fue accesible después de la descarga")

except Exception as e:
    pasos.append(f"Error inesperado: {str(e)}")
finally:
    driver.quit()
    generar_reporte("Descarga de video desde grid", pasos, success)
