from django.utils.translation import gettext as _
from django.db import models


class OutputChannelChoice(models.IntegerChoices):
    """Поддерживаемые системой варианты отправки сообщения."""
    SOME_API_MESSAGE = 0, _('API (api/message/)')
    """Через запрос POST api/message/"""
    EMAIL = 1, _('Электронная почта')
    """Отправка на почту"""
    SMS = 2, _('SMS')
    """Отправка SMS"""
