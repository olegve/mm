from django.test import TestCase
from django.conf import settings


class SettingsTestCase(TestCase):

    def test_HTTP_X_API_KEY(self):
        header = 'API_KEY_CUSTOM_HEADER'
        self.assertEqual(
            hasattr(settings, header),
            True,
            f'В настройках приложения (settings.py) отсутствует переменная {header}'
        )
        header_value = 'HTTP_X_API_KEY'
        self.assertEqual(
            header_value,
            settings.API_KEY_CUSTOM_HEADER,
            f'Неверное конфигурирование.  '
            f'В settings.py должна быть строка {header}="{header_value}", '
            f'а не {header}="{settings.API_KEY_CUSTOM_HEADER}".'
        )

