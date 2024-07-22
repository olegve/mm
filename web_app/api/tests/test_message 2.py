import json
import logging

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from core.tests.api_key import get_api_key_for_blocked_organization, get_api_key_for_organization
from core.tests.client import get_client_with_api_key_header


class ApiMessageTestCase(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = reverse('message')

    def test_get_anonymous_request(self):
        response = self.client.post(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, 'Неавторизованый домтуп закрыт.')

    def test_get_blocked_organization_token_request(self):
        key = get_api_key_for_blocked_organization('Тест')
        client = get_client_with_api_key_header(key.key)
        response = client.post(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, 'Неавторизованый домтуп закрыт.')

    def test_get_authorized_with_wrong_request(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)
        response = client.post(self.url)
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)
        response = client.get(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = client.put(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = client.patch(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = client.delete(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = client.head(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = client.options(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_authorized_request(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Пробуем запрос с нормальными данными
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "subject": "Это поле длиной не более 50 символов. 123456789012",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')

        # TODO: Написать тесты на правильный ответ

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_authorized_request_with_wrong_priority_entry(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Пробуем запросы с неправильными данными (несуществующий приоритет)
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 200
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_with_wrong_message_type_1(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Пробуем запросы с неправильными данными (неверный тип данных)
        data = json.dumps({
            "message": {
                "message": ["Большой перепад давления, возможно пора заменить фильтр"],
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_with_wrong_message_type_2(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        data = json.dumps({
            "message": {
                "message": 35,
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_without_message(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Пробуем запросы с неправильными данными (отсутствует поле "message")
        data = json.dumps({
            "message": {

                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_without_note(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # А если отсутствует опциоеальное поле "note", то всё нормально
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",

                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_authorized_request_with_priority_as_string(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Если приоритет передаётся не числом, а строкой, то Pydantic тоже нормально справляется с этим
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": "2"
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_authorized_request_with_wrong_main_field_name(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Пробуем запросы с неправильными полями
        data = json.dumps({
            "message_bad": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_with_wrong_message_field_name(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        data = json.dumps({
            "message": {
                "message_bad": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_with_wrong_note_field_name(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # А если поле "note" неверно названо, то оно просто игнорируется, так как оно опциональное
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note_bad": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_authorized_request_with_wrong_building_field_name(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building_bad": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_with_wrong_system_field_name(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system_bad": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_with_wrong_node_field_name(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node_bad": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)

    def test_get_authorized_request_with_wrong_priority_field_name(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Если нет поля "priority", то оно генирится со значением по умлчанию.
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority_bad": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_optional_subject_field(self):
        key = get_api_key_for_organization('Тест')
        client = get_client_with_api_key_header(key.key)

        # Пробуем запрос с нормальными данными
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "subject": "Это поле длиной не более 50 символов. 123456789012",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code, 'Правильное сообщение. Запрос должен проходить.')

        # Пробуем запрос с полем "subject", размером больше, чем 50 разрешённых символов
        data = json.dumps({
            "message": {
                "message": "Большой перепад давления, возможно пора заменить фильтр",
                "subject": "Это поле длиной не более 50 символов. 123456789012!",
                "note": "Примечания к сообщению",
                "building": "Покровка, 5",
                "system": "К10-В10",
                "node": "воздушный фильтр №1",
                "priority": 2
            }
        })
        response = client.generic(method="POST", path=f"{self.url}", data=data, content_type='application/json')
        self.assertEqual(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            response.status_code,
            'Слишком длинное поле "subject". Размер не более 50 символов. Запрос не должен проходить.'
        )
