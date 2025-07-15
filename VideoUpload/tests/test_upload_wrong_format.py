# tests/test_upload_wrong_format.py
import sys
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.pdf_report import generar_reporte

TEST_EMAIL = "ddelgadoprofe@unal.edu.co"
TEST_PASSWORD = "1234"
FRONTEND_URL = "http://localhost:3000"
UPLOAD_URL = "http://localhost:3000/upload"
WRONG_FILE = os.path.abspath("media/test_file.txt")
pasos = []
success = False

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

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 10)

try:
    driver.get(FRONTEND_URL)
    time.sleep(1)
    driver.execute_script(f"localStorage.setItem('token', '{token}');")
    driver.execute_script(f"localStorage.setItem('user_id', '{user_id}');")
    pasos.append("Token y user_id insertados en localStorage del navegador")

    driver.get(UPLOAD_URL)
    time.sleep(2)

    print("[1] Llenando formulario con archivo .txt...")
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Título del video']").send_keys("Archivo inválido")
    driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Descripción']").send_keys("Intento con .txt")
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Etiquetas (separadas por coma)']").send_keys("txt,test")
    driver.find_element(By.ID, "file-upload").send_keys(WRONG_FILE)
    pasos.append("Formulario llenado con archivo de formato no válido")

    print("[2] Enviando formulario...")
    driver.find_element(By.CSS_SELECTOR, "button.upload-button").click()
    time.sleep(1)

    error_msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "upload-message")))
    if "error" in error_msg.text.lower():
        pasos.append("Error detectado correctamente por formato inválido")
        success = True
    else:
        pasos.append("No se detectó el error esperado")

except Exception as e:
    pasos.append(f"Error inesperado: {str(e)}")
finally:
    driver.quit()
    generar_reporte("Falla por formato inválido", pasos, success)
