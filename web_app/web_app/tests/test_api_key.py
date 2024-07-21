# import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
import logging

from django.db import IntegrityError
from rest_framework.test import APITestCase

from organizations.models import Organization
from core.tests.api_key import get_api_key_for_organization, get_api_key_for_blocked_organization


class ApiKeyTestCase(APITestCase):
    def test_get_api_key_for_organization(self):
        name = "ForestHill"
        key = get_api_key_for_organization(name)
        self.assertEqual(name, key.organization_name, f'Имя организации должно быть {name}')
        count = Organization.objects.filter(name=name).count()
        self.assertEqual(1, count, 'Найдено не верное количество организаций.')
        organization = Organization.objects.get(name=name)
        self.assertEqual(name, organization.name, f'Имя организации должно быть {name}')
        self.assertEqual(organization.id, key.organization_id, 'Неправильный идентификатор организации')
        organization_api_key = organization.api_keys.get(name=key.api_key_name)
        self.assertEqual(organization_api_key.prefix, key.api_key_instance.prefix, 'Неверный преыикс API ключа')

    def test_integrity_error(self):
        id1 = '213531748'
        key1 = get_api_key_for_organization('test1', id=id1)
        key2 = get_api_key_for_organization('test2', id='9283645014')
        with self.assertRaises(IntegrityError, msg='Система не должна давать создавать организации с одинаковыми id'):
            get_api_key_for_organization('test1', id=id1)

    def test_api_key_is_active(self):
        key = get_api_key_for_organization('test1')

        # Проверка временной блокировки
        key.api_key_instance.blocked = True
        self.assertFalse(key.api_key_instance.is_active, f'API ключ {key.api_key_name} не должен быть активным.')
        key.api_key_instance.blocked = False
        self.assertTrue(key.api_key_instance.is_active, f'API ключ {key.api_key_name} должен быть активным.')

        # Проверка на истечение срока давности
        now = datetime.now()
        now_with_tz = now.astimezone()
        key.api_key_instance.expiry_date = now_with_tz - relativedelta(years=1)
        self.assertFalse(key.api_key_instance.is_active, f'API ключ {key.api_key_name} не должен быть активным.')
        key.api_key_instance.expiry_date = now_with_tz + relativedelta(years=1)
        self.assertTrue(key.api_key_instance.is_active, f'API ключ {key.api_key_name} должен быть активным.')
        key.api_key_instance.expiry_date = None
        self.assertTrue(key.api_key_instance.is_active, f'API ключ {key.api_key_name} должен быть активным.')

        # Проверка отзыва API ключа
        key.api_key_instance.revoked = True
        self.assertFalse(key.api_key_instance.is_active, f'API ключ {key.api_key_name} не должен быть активным.')

        # Проверка блокировки организации
        blocked_key = get_api_key_for_blocked_organization('test2')
        self.assertFalse(
            blocked_key.api_key_instance.is_active,
            f'API ключ {blocked_key.api_key_name} не должен быть активным.'
        )

