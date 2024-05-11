from django.db import models
from django.utils.translation import gettext as _


# ACTIVE = 0
# """Статус компании. Компания активна.  API Keys активны."""
# BLOCKED = 1
# """Статус компании. Компания заблокирована по какой либо причине. API Keys заблокированы."""
# PARTIAL = 2
# """Статус компании. Компания частично заблокирована по какой либо причине. API Keys заблокированы."""
# ARCHIVE = 3
# """
# Статус компании. Компания заблокирована по какой либо причине.  API Keys заблокированы.
# Пользователи заблокированы.
# """
#
# STATE_CHOICES: tuple[tuple[int, str], ...] = (
#     (ACTIVE,  'Активна'),
#     (BLOCKED, 'Заблокирована'),
#     (PARTIAL, 'Заблокирована частично'),
#     (ARCHIVE, 'Архив'),
# )
# """Поддерживаемые варианты статусов состояния организации в системе."""


class OrganizationStateChoice(models.IntegerChoices):
    """Поддерживаемые варианты статусов состояния организации в системе."""
    ACTIVE = 0, 'Активна'
    """Компания активна.  API Keys активны."""
    BLOCKED = 1, 'Заблокирована'
    """Компания заблокирована по какой либо причине. API Keys заблокированы."""
    PARTIAL = 2, 'Заблокирована частично'
    """Компания частично заблокирована по какой либо причине. API Keys заблокированы."""
    ARCHIVE = 3, 'В архиве'
    """
    Компания заблокирована по какой либо причине.  API Keys заблокированы.  
    Пользователи заблокированы.
    """
    __empty__ = _("(Unknown)")
    """Пустое значение, котороко быть не должно"""


if __name__ == "__main__":
    print(OrganizationStateChoice.ACTIVE)
    print(OrganizationStateChoice.ACTIVE.value)
    print(OrganizationStateChoice.ACTIVE.label)
    print(OrganizationStateChoice(2).label)
    print(OrganizationStateChoice(2).name)
