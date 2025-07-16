import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_login_success(test_results):
    test_name = "test_login_success"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "email": "test@example.com",
        "password": "P@ssword1"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/login", json=payload, headers=headers)
    duration = round(time.time() - start_time, 3) 

    try:
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
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

def test_login_invalid(test_results):
    test_name = "test_login_invalid"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "email": "wrong@example.com",
        "password": 9999
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/login", json=payload, headers=headers)
    duration = round(time.time() - start_time, 3) 

    try:
        assert response.status_code == 401
        data = response.json()
        assert data.get("message") == "Incorrect user or password"
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