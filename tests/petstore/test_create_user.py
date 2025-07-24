import pytest
import requests
import json
from jsonschema import validate
from client import PetstoreClient

BASE_URL = "https://petstore.swagger.io/v2"
USER_ENDPOINT = f"{BASE_URL}/user"

# 1. Functional tests
#Happy path: create user with valid data
def test_create_user_valid(valid_user_payload):
    username = valid_user_payload["username"]
    response = requests.post(USER_ENDPOINT, json=valid_user_payload)
    body = response.json()

    #print(body)
    assert response.status_code == 200
    with open("schemas/post_create_user.json") as file:
        validate(body, schema=json.loads(file.read()))
    assert response.json()["message"] == str(valid_user_payload["id"])

    # Verify user is created
    get_response = requests.get(f"{USER_ENDPOINT}/{username}")
    assert get_response.status_code == 200

# Create user twice with the same id
def test_create_user_with_same_id_twice(valid_user_payload):
    #first user creation
    response = requests.post(USER_ENDPOINT, json=valid_user_payload)
    body = response.json()
    assert response.status_code == 200

    #second user creation
    response2 = requests.post(USER_ENDPOINT, json=valid_user_payload)
    assert response.status_code == 400

def test_create_user_without_auth():
    assert False, "TODO: Need to clarify requirements about work of this endpoint without auth"

# 2. Missing required field
@pytest.mark.parametrize("missing_field", [
    "id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"
])
def test_create_user_missing_field(valid_user_payload, missing_field):
    payload = valid_user_payload.copy()
    payload.pop(missing_field)
    response = PetstoreClient.create_user(payload)
    assert response.status_code == 400

# 3. Invalid data type
def test_create_user_invalid_id_type(valid_user_payload):
    payload = valid_user_payload.copy()
    payload["id"] = "notanumber"

    response = requests.post(USER_ENDPOINT, json=payload)
    assert response.status_code == 400

# 4. Body is missed
def test_create_user_missing_body():
    response = requests.post(USER_ENDPOINT)
    assert response.status_code in [400, 415]
