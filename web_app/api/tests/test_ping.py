import logging

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from api.models import OrganizationAPIKey
from organizations.models import Organization


class ApiPingTestCase(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = reverse('ping')

    def _required_response_fields_test(self, response):
        value = response.data.get('ping', None)
        self.assertEqual(value is not None, True, f'Словарь должен содержать ключ ["ping"].')
        self.assertEqual('pong', value, f'Значение поля ["ping"] должно быть "pong".')
        value = response.data.get('timestamp', None)
        self.assertEqual(value is not None, True, f'Словарь должен содержать ключ ["timestamp"].')
        value = response.data.get('time_zone', None)
        self.assertEqual(value is not None, True, f'Словарь должен содержать ключ ["time_zone"].')

    def _required_response_organization_fields_test(self, response):
        count = len(response.data.keys())
        self.assertEqual(4, count, f'В словаре должно быть четыре записи, а не {count}.')
        value = response.data.get('organization', None)
        self.assertEqual(value is not None, True, f'Словарь должен содержать ключ ["organization"].')
        value = value.get('name', None)
        self.assertEqual(
            value is not None,
            True,
            f'Словарь ["organization"] должен содержать ключ ["name"].'
        )

    def test_get_HTTP_200(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_anonymous_request(self):
        response = self.client.get(self.url)
        count = len(response.data.keys())
        self.assertEqual(3, count, f'В словаре должно быть три записи, а не {count}.')
        self._required_response_fields_test(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_unknown_token_request(self):
        client = APIClient()
        headers = {'HTTP_X_API_KEY': 'Any APY Key'}
        client.credentials(**headers)
        response = client.get(self.url)
        self._required_response_fields_test(response)
        self._required_response_organization_fields_test(response)
        self.assertEqual(
            'unknown',
            response.data.get('organization').get('name'),
            f'Значение поля ["organization"]["name"] должно быть "unknown".'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_known_token_request(self):
        organization_name = 'Test'
        organization = Organization.objects.create(name=organization_name)
        api_key, key = OrganizationAPIKey.objects.create_key(name="key-test-service", organization=organization)
        client = APIClient()
        headers = {'HTTP_X_API_KEY': key}
        client.credentials(**headers)
        response = client.get(self.url)
        self._required_response_fields_test(response)
        self._required_response_organization_fields_test(response)
        self.assertEqual(
            organization_name,
            response.data.get('organization').get('name'),
            f'Значение поля ["organization"]["name"] должно быть "{organization_name}".'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)


