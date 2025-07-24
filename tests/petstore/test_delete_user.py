import pytest
import requests
import json
from jsonschema import validate

BASE_URL = "https://petstore.swagger.io/v2"
USER_ENDPOINT = f"{BASE_URL}/user"

# 1. Successful deletion of an existing user
def test_delete_user_success(valid_user_payload):
    username = "testuser_delete"
    # Create the user first
    payload = payload = valid_user_payload.copy()
    payload["username"] = username

    requests.post(f"{USER_ENDPOINT}", json=payload)
    # Verify user is created
    get_response = requests.get(f"{USER_ENDPOINT}/{username}")
    assert get_response.status_code == 200
    # Delete the user
    response = requests.delete(f"{USER_ENDPOINT}/{username}")
    assert response.status_code == 200
    body = response.json()
    with open("schemas/put_update_user.json") as file:
        validate(body, schema=json.loads(file.read()))
    # Verify user is deleted
    get_response = requests.get(f"{USER_ENDPOINT}/{username}")
    assert get_response.status_code == 404

# 2. Deletion of a non-existent user
def test_delete_nonexistent_user():
    username = "user_does_not_exist_54321"
    response = requests.delete(f"{USER_ENDPOINT}/{username}")
    assert response.status_code == 404

# 3. Attempt to delete with invalid username (empty string)
def test_delete_user_invalid_username():
    username = ""
    response = requests.delete(f"{USER_ENDPOINT}/{username}")

    assert response.status_code in [404, 405]

