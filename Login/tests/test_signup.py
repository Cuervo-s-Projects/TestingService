import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_signup_success(results):
    test_name = "test_signup_success"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "P@ssword1",
        "password_confirm": "P@ssword1",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 201
        data = response.json()
        assert data.get("message") == "User successfully created"
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

def test_signup_password_mismatch(results):
    test_name = "test_signup_password_mismatch"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "P@ssword1",
        "password_confirm": "P@ssword2",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Passwords do not match"
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

def test_signup_password_least_characters(results):
    test_name = "test_signup_password_least_characters"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "P@ss1",
        "password_confirm": "P@ss1",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Password must be at least 6 characters"
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

def test_signup_password_uppercase_letter(results):
    test_name = "test_signup_password_uppercase_letter"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "p@ssword1",
        "password_confirm": "p@ssword1",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Password must include at least one uppercase letter"
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

def test_signup_password_uppercase_letter(results):
    test_name = "test_signup_password_uppercase_letter"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "p@ssword1",
        "password_confirm": "p@ssword1",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Password must include at least one uppercase letter"
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

def test_signup_password_lowercase_letter(results):
    test_name = "test_signup_password_lowercase_letter"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "P@SSWORD1",
        "password_confirm": "P@SSWORD1",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Password must include at least one lowercase letter"
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

def test_signup_password_number(results):
    test_name = "test_signup_password_number"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "P@ssword",
        "password_confirm": "P@ssword",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Password must include at least one number"
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

def test_signup_special_character(results):
    test_name = "test_signup_special_character"
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Password1",
        "password_confirm": "Password1",
        "last_name": "Test",
        "first_name": "User",
        "age": 20,
        "date_birth": "2005-01-01"
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/api/signup", json=payload)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 400
        data = response.json()
        assert data.get("message") == "Password must include at least one special character"
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