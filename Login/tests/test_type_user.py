import requests
import jwt
import datetime
import time

BASE_URL = "http://127.0.0.1:5000"
JWT_SECRET_KEY = "t2$Z#rP8vL@xJ!k93^bE*Wz67sQuNmd1YhaXG+!RQvPb"
JWT_ALGORITHM = "HS256"

def generate_fake_jwt(email):
    payload = {
        "sub": email
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token

def test_type_user(results):
    test_name = "test_type_user"
    token = generate_fake_jwt("test@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/type_user", headers=headers)
    duration = round(time.time() - start_time, 3)

    try:
        assert response.status_code == 200
        data = response.json()
        rol = data.get("roles")[0]
        assert rol == "student"
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
