# tests/upload_video_test.py
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from utils.pdf_report import generar_reporte

# Config
FRONTEND_URL = "http://localhost:3000"
UPLOAD_URL = f"{FRONTEND_URL}/upload"
DELETE_URL = "http://localhost:5001/videos"
VIDEO_PATH = os.path.abspath("media/test_video.mp4")
TEST_EMAIL = "ddelgadoprofe@unal.edu.co"
TEST_PASSWORD = "1234"

pasos = []
video_id_subido = None

# 1. Obtener token y user_id desde backend
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

# 2. Setup Selenium
options = Options()
options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

try:
    print("[1] Inyectando localStorage y abriendo app...")
    driver.get(FRONTEND_URL)
    driver.execute_script(f"""
        window.localStorage.setItem('token', '{token}');
        window.localStorage.setItem('user_id', '{user_id}');
    """)
    pasos.append("Credenciales inyectadas en localStorage")

    time.sleep(1)

    print("[2] Entrando a /upload directamente...")
    driver.get(UPLOAD_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Sube tu video')]")))
    pasos.append("Página de subida cargada")

    print("[3] Llenando formulario...")
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Título del video']").send_keys("Video sin login visual")
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Descripción']").send_keys("Video subido directamente")
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Etiquetas (separadas por coma)']").send_keys("selenium,testing")
    time.sleep(0.5)

    file_input = driver.find_element(By.ID, "file-upload")
    file_input.send_keys(VIDEO_PATH)
    pasos.append("Formulario completado")

    print("[4] Subiendo video...")
    driver.find_element(By.CSS_SELECTOR, "button.upload-button").click()
    pasos.append("Botón de subir presionado")

    print("[5] Esperando confirmación...")
    msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "upload-message")))
    assert "subido correctamente" in msg.text.lower()
    pasos.append("Mensaje de éxito recibido")

    print("[6] Buscando ID para eliminar...")
    res = requests.get("http://localhost:5001/videos")
    videos = res.json().get("videos", [])
    for v in videos:
        if v["title"] == "Video sin login visual":
            video_id_subido = v["_id"]
            pasos.append(f"Video ID: {video_id_subido}")
            break

    if video_id_subido:
        del_res = requests.delete(f"{DELETE_URL}/{video_id_subido}")
        if del_res.ok:
            pasos.append("Video eliminado correctamente")
        else:
            pasos.append("Fallo al eliminar video")
    else:
        pasos.append("No se encontró el ID del video")

    success = True

except Exception as e:
    pasos.append(f"Error: {str(e)}")
    success = False

finally:
    driver.quit()
    generar_reporte(
        nombre_prueba="Subida directa (sin login visual)",
        pasos=pasos,
        exitoso=success
    )
