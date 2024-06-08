# from abc import abstractmethod
# from typing import NamedTuple, Any, Optional
from enum import Enum, IntEnum

from django.db import models
from django.utils.translation import gettext as _

# import api.models
# from api.models import Message
# from api.services.message import APIDataConverter
# from core.input_channel import InputChannelChoice


class PriorityEnum(IntEnum):
    """Поддерживаемые варианты приоритетов сообщений в системе."""
    URGENT = 0  # 0 - Celery priority
    """Сверхвысокий приоритет.  Возможны катастрофические последствия."""
    HIGH = 1    # 2 - Celery priority
    """Высокий приоритет.  Необходимо безотлагательно решить возникшую проблему"""
    NORMAL = 2  # 4 - Celery priority
    """Обычный приоритет."""
    LOW = 3     # 6 - Celery priority
    """Низкий приоритет.   Можно временно отложить решение проблемы."""
    NO = 4      # 8 - Celery priority
    """Информационное сообщение. Проблемы отсутствуют."""


class PriorityChoice(models.IntegerChoices):
    """Поддерживаемые варианты приоритетов сообщений в системе."""
    URGENT = PriorityEnum.URGENT, _('Срочный')
    """Сверхвысокий приоритет.  Возможны катастрофические последствия."""
    HIGH = PriorityEnum.HIGH, _('Высокий')
    """Высокий приоритет.  Необходимо безотлагательно решить возникшую проблему"""
    NORMAL = PriorityEnum.NORMAL, _('Стандартный приоритет.')
    """Обычный приоритет."""
    LOW = PriorityEnum.LOW, _('Низкий')
    """Низкий приоритет.   Можно временно отложить решение проблемы."""
    NO = PriorityEnum.NO, _('Отсутствует')
    """Информационное сообщение. Проблемы отсутствуют."""
    __empty__ = _("(Unknown)")
    """Пустое значение, котороко быть не должно"""







