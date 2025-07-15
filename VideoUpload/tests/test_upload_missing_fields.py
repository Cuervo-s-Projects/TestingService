# tests/test_upload_missing_fields.py
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

    print("[1] Solo se llena el título...")
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Título del video']").send_keys("Fallo campos vacíos")
    pasos.append("Solo se llenó el título")

    print("[2] Intentando subir sin los demás campos...")
    driver.find_element(By.CSS_SELECTOR, "button.upload-button").click()
    time.sleep(1)

    error_msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "upload-message")))
    if "completa todos los campos" in error_msg.text.lower():
        pasos.append("Error detectado correctamente")
        success = True
    else:
        pasos.append("Mensaje inesperado: " + error_msg.text)

except Exception as e:
    pasos.append(f"Error inesperado: {str(e)}")
finally:
    driver.quit()
    generar_reporte("Falla por campos incompletos", pasos, success)
