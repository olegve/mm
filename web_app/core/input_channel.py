from django.utils.translation import gettext as _
from django.db import models


class InputChannelChoice(models.IntegerChoices):
    """Поддерживаемые варианты приоритетов сообщений в системе."""
    API_MESSAGE = 0, _('API (api/message/)')
    """Через запрос POST api/message/"""

