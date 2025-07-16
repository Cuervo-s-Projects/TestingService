import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_username_found(results):
    test_name = "test_username_found"

    payload = {"id": "6858a9d9c1e99b58e1659dc5"}

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/username", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 200
        data = response.json()
        assert data.get("username") == "luis"
        results.append({
            "name": test_name,
            "status": "PASSED",
            "code": response.status_code,
            "response": data,
            "duration": duration
        })
    except AssertionError:
        results.append({
            "name": test_name,
            "status": "FAILED",
            "code": response.status_code,
            "response": response.text,
            "duration": duration
        })

def test_username_not_found(results):
    test_name = "test_username_not_found"

    payload = {"id": "invalid"}

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/username", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "User not found"
        results.append({
            "name": test_name,
            "status": "PASSED",
            "code": response.status_code,
            "response": data,
            "duration": duration
        })
    except AssertionError:
        results.append({
            "name": test_name,
            "status": "FAILED",
            "code": response.status_code,
            "response": response.text,
            "duration": duration
        })
