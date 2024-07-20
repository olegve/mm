from rest_framework.test import APIClient


def get_client_with_api_key_header(key: str, key_header: str = 'HTTP_X_API_KEY') -> APIClient:
    client = APIClient()
    headers = {key_header: key}
    client.credentials(**headers)
    return client

