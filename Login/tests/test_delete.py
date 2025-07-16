import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_delete_success(test_results):
    test_name = "test_login_success"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    correo= "test@example.com"

    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/delete/{correo}", headers=headers)
    duration = round(time.time() - start_time, 3) 

    try:
        assert response.status_code == 200
        data = response.json()
        assert data.get("message") == "Successful elimination"
        test_results.append({
            "name": test_name,
            "status": "PASSED",
            "code": response.status_code,
            "response": data,
            "duration": duration
        })
    except AssertionError:
        test_results.append({
            "name": test_name,
            "status": "FAILED",
            "code": response.status_code,
            "response": response.text,
            "duration": duration
        })

def test_delete_invalid(test_results):
    test_name = "test_login_invalid"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    correo= "wrong@example.com"

    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/delete/{correo}", headers=headers)
    duration = round(time.time() - start_time, 3) 

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Invalid email"
        test_results.append({
            "name": test_name,
            "status": "PASSED",
            "code": response.status_code,
            "response": data,
            "duration": duration
        })
    except AssertionError:
        test_results.append({
            "name": test_name,
            "status": "FAILED",
            "code": response.status_code,
            "response": response.text,
            "duration": duration
        })