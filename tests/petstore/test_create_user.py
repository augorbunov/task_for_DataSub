import pytest
import requests
import json
from jsonschema import validate

BASE_URL = "https://petstore.swagger.io/v2"
USER_ENDPOINT = f"{BASE_URL}/user"

# 1. Functional tests
#Happy path: create user with valid data
def test_create_user_valid():
    username = "testuser12345"
    payload = {
        "id": 12345,
        "username": username,
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser12345@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    body = response.json()

    #print(body)
    assert response.status_code == 200
    with open("schemas/post_create_user.json") as file:
        validate(body, schema=json.loads(file.read()))
    assert response.json()["message"] == str(payload["id"])

    # Verify user is created
    get_response = requests.get(f"{USER_ENDPOINT}/{username}")
    assert get_response.status_code == 200

# Create user twice with the same id
def test_create_user_with_same_id_twice():
    payload = {
        "id": 12345,
        "username": "testuser12345",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser12345@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    #first user creation
    response = requests.post(USER_ENDPOINT, json=payload)
    body = response.json()
    assert response.status_code == 200

    #second user creation
    response2 = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_without_auth():
    assert False, "TODO: Need to clarify requirements about work of this endpoint without auth"

# 2. Missing required field
def test_create_user_missing_id():
    payload = {
        #"id" is missing
        "username": "testuser12345",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser12345@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_missing_username():
    payload = {
        "id": 12346,
        # "username" is missing
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser_missing@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_missing_first_name():
    payload = {
        "id": 12345,
        "username": "testuser12345",
        #"firstName" is missing
        "lastName": "User",
        "email": "testuser12345@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_missing_last_name():
    payload = {
        "id": 12345,
        "username": "testuser12345",
        "firstName": "Test",
        #"lastName" is missing
        "email": "testuser12345@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_missing_email():
    payload = {
        "id": 12345,
        "username": "testuser12345",
        "firstName": "Test",
        "lastName": "User",
        #"email" is missing
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_missing_password():
    payload = {
        "id": 12345,
        "username": "testuser12345",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser12345@example.com",
        #"password" is missing
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_missing_phone():
    payload = {
        "id": 12345,
        "username": "testuser12345",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser12345@example.com",
        "password": "password123",
        #"phone" is missing
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

def test_create_user_missing_user_status():
    payload = {
        "id": 12345,
        "username": "testuser12345",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser12345@example.com",
        "password": "password123",
        "phone": "1234567890"
        #"userStatus" is missing
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

# 3. Invalid data type
def test_create_user_invalid_id_type():
    payload = {
        "id": "notanumber",
        "username": "testuser_invalidid",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser_invalidid@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }
    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

# 4. Body is missed
def test_create_user_missing_body():
    response = requests.post(USER_ENDPOINT)
    assert response.status_code in [400, 415]
