# tests/petstore/conftest.py
import pytest

@pytest.fixture
def valid_user_payload():
    return {
        "id": 12345,
        "username": "testuser12345",
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser12345@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }