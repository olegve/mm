from enum import IntEnum

from django.db import models
from django.utils.translation import gettext as _


class OrganizationStateEnum(IntEnum):
    """Поддерживаемые варианты статусов состояния организации в системе.  Для совместимости с Pydantic"""
    ACTIVE = 0
    """Компания активна.  API Keys активны."""
    BLOCKED = 1
    """Компания заблокирована по какой либо причине. API Keys заблокированы."""
    PARTIAL = 2
    """Компания частично заблокирована по какой либо причине. API Keys заблокированы."""
    ARCHIVE = 3
    """
    Компания заблокирована по какой либо причине.  API Keys заблокированы.  
    Пользователи заблокированы.
    """


class OrganizationStateChoice(models.IntegerChoices):
    """Поддерживаемые варианты статусов состояния организации в системе."""
    ACTIVE = OrganizationStateEnum.ACTIVE, _('Активна')
    """Компания активна.  API Keys активны."""
    BLOCKED = OrganizationStateEnum.BLOCKED, _('Заблокирована')
    """Компания заблокирована по какой либо причине. API Keys заблокированы."""
    PARTIAL = OrganizationStateEnum.PARTIAL, _('Заблокирована частично')
    """Компания частично заблокирована по какой либо причине. API Keys заблокированы."""
    ARCHIVE = OrganizationStateEnum.ARCHIVE, _('В архиве')
    """
    Компания заблокирована по какой либо причине.  API Keys заблокированы.  
    Пользователи заблокированы.
    """


if __name__ == "__main__":
    print(OrganizationStateChoice.ACTIVE)
    print(OrganizationStateChoice.ACTIVE.value)
    print(OrganizationStateChoice.ACTIVE.label)
    print(OrganizationStateChoice(2).label)
    print(OrganizationStateChoice(2).name)
