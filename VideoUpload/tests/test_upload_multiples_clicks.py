import sys
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Para el reporte PDF
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.pdf_report import generar_reporte

TEST_EMAIL = "ddelgadoprofe@unal.edu.co"
TEST_PASSWORD = "1234"
VIDEO_PATH = os.path.abspath("media/test_video.mp4")
FRONTEND_URL = "http://localhost:3000"
UPLOAD_URL = "http://localhost:3000/upload"
API_URL = "http://localhost:5001/videos"
pasos = []
success = False

# 1. Autenticación vía backend
try:
    print("[0] Autenticando vía API...")
    res = requests.post("http://localhost:5000/api/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })
    token = res.json()["access_token"]
    profile = requests.get("http://localhost:5000/api/profile", headers={
        "Authorization": f"Bearer {token}"
    })
    user_id = profile.json()["_id"]
    pasos.append("Token y user_id obtenidos vía backend")
except Exception as e:
    print("Error al autenticar:", e)
    exit(1)

# 2. Configurar Selenium
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 10)

try:
    # 3. Abrir primero la raíz para insertar token
    driver.get(FRONTEND_URL)
    time.sleep(1)
    driver.execute_script(f"localStorage.setItem('token', '{token}');")
    driver.execute_script(f"localStorage.setItem('user_id', '{user_id}');")
    pasos.append("Token y user_id insertados en localStorage del navegador")

    # 4. Ir a /upload
    driver.get(UPLOAD_URL)
    time.sleep(2)

    print("[1] Llenando formulario completo...")
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Título del video']").send_keys("Video clic doble")
    driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Descripción']").send_keys("Prueba doble clic")
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Etiquetas (separadas por coma)']").send_keys("doble,test")
    driver.find_element(By.ID, "file-upload").send_keys(VIDEO_PATH)
    pasos.append("Formulario llenado")

    print("[2] Clic varias veces en subir...")
    subir_btn = driver.find_element(By.CSS_SELECTOR, "button.upload-button")
    subir_btn.click()
    time.sleep(0.5)
    subir_btn.click()
    time.sleep(0.5)
    subir_btn.click()
    pasos.append("Botón presionado varias veces")

    print("[3] Esperando mensaje de éxito...")
    success_msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "upload-message")))
    if "subido correctamente" in success_msg.text.lower():
        pasos.append("Mensaje de éxito detectado")

    print("[4] Verificando duplicados en la base de datos...")
    res = requests.get(API_URL)
    videos = [v for v in res.json()["videos"] if v["title"] == "Video clic doble"]
    pasos.append(f"{len(videos)} videos encontrados con el mismo título")

    if len(videos) == 1:
        pasos.append("No se duplicó el video")
        success = True
    else:
        pasos.append("El video fue subido más de una vez")

    for v in videos:
        requests.delete(f"{API_URL}/{v['_id']}")
        pasos.append(f"Video {v['_id']} eliminado")

except Exception as e:
    pasos.append(f"Error inesperado: {str(e)}")
finally:
    driver.quit()
    generar_reporte("Falla por múltiples clics", pasos, success)
