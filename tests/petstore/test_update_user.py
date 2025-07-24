import pytest
import requests
import json
from jsonschema import validate

BASE_URL = "https://petstore.swagger.io/v2"
USER_ENDPOINT = f"{BASE_URL}/user"

# 1. Functional tests
# Successful update of an existing user
def test_update_user_success(valid_user_payload):
    username = valid_user_payload["username"]
    # First, create the user to ensure it exists
    requests.post(f"{USER_ENDPOINT}", json=valid_user_payload)
    # Now, update the user
    update_payload = {
        "id": 20002,
        "username": username,
        "firstName": "NewFirst",
        "lastName": "NewLast",
        "email": "new@example.com",
        "password": "newpass",
        "phone": "1111111111",
        "userStatus": 2
    }
    response = requests.put(f"{USER_ENDPOINT}/{username}", json=update_payload)
    assert response.status_code == 200
    body = response.json()
    with open("schemas/put_update_user.json") as file:
        validate(body, schema=json.loads(file.read()))
    assert body["message"] == str(update_payload["id"])

    # Validate that all values have been updated to new
    get_response = requests.get(f"{USER_ENDPOINT}/{username}")
    user_data = get_response.json()
    for key in update_payload:
        assert user_data[key] == update_payload[key], f"Field {key} did not update correctly"

# Update user name
def test_update_user_name_failed(valid_user_payload):
    username = valid_user_payload["username"]
    # create the user to ensure it exists
    requests.post(f"{USER_ENDPOINT}", json=valid_user_payload)
    # update the user name
    update_payload = valid_user_payload.copy()
    update_payload["username"] = "testuser_update_new"
    response = requests.put(f"{USER_ENDPOINT}/{username}", json=update_payload)
    assert response.status_code == 400


# 2. Update with missing required fields
def test_update_user_missing_username(valid_user_payload):
    username = valid_user_payload["username"]
    update_payload = valid_user_payload.copy()
    update_payload.pop("username")

    response = requests.put(f"{USER_ENDPOINT}/{username}", json=update_payload)
    assert response.status_code == 400

# 3. Update with invalid data types
def test_update_user_invalid_id_type():
    username = "testuser_update_invalidid"
    update_payload = {
        "id": "notanumber",
        "username": username,
        "firstName": "NewFirst",
        "lastName": "NewLast",
        "email": "new@example.com",
        "password": "newpass",
        "phone": "1111111111",
        "userStatus": 2
    }
    response = requests.put(f"{USER_ENDPOINT}/{username}", json=update_payload)
    assert response.status_code == 400

# 4. Update a non-existent user
def test_update_nonexistent_user():
    username = "user_does_not_exist_12345"

    #Verify that user not exist
    response = requests.get(f"{USER_ENDPOINT}/{username}")
    assert response.status_code == 404

    update_payload = {
        "id": 99999,
        "username": username,
        "firstName": "Ghost",
        "lastName": "User",
        "email": "ghost@example.com",
        "password": "ghostpass",
        "phone": "9999999999",
        "userStatus": 0
    }
    response = requests.put(f"{USER_ENDPOINT}/{username}", json=update_payload)
    assert response.status_code == 404
    #Verify that user not exist
    response = requests.get(f"{USER_ENDPOINT}/{username}")
    assert response.status_code == 404

