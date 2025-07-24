# tests/petstore/client.py
import requests

class PetstoreClient:
    BASE_URL = "https://petstore.swagger.io/v2"
    USER_ENDPOINT = f"{BASE_URL}/user"

    @staticmethod
    def create_user(payload):
        return requests.post(PetstoreClient.USER_ENDPOINT, json=payload)

    @staticmethod
    def get_user(username):
        return requests.get(f"{PetstoreClient.USER_ENDPOINT}/{username}")

    @staticmethod
    def delete_user(username):
        return requests.delete(f"{PetstoreClient.USER_ENDPOINT}/{username}")

    @staticmethod
    def update_user(username, payload):
        return requests.put(f"{PetstoreClient.USER_ENDPOINT}/{username}", json=payload)