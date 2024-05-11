from typing import Optional

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _

from rest_framework_api_key.models import AbstractAPIKey

from pydantic import BaseModel, Field

from api.api_key import OrganizationAPIKeyManager
from core.message import PriorityChoice, PriorityEnum
from core.organization_state import OrganizationStateChoice
from organizations.models import Organization


class OrganizationAPIKey(AbstractAPIKey):
    """Модель, содержащая API ключи организаций.

        Наследуется от AbstractAPIKey.

        Attributes:
            id(str):
                Нередактируемое поле.
            prefix(str):
                Нередактируемое поле.
            hashed_key(str):
                Нередактируемое поле.
            created(datetime):
                Дата и время создания ключа.
                Создаётся автоматически.
                Нередактируемое поле.
            name(str):
                Имя ключа.
                Поле должно быть уникальным для каждой организации.
            revoked(bool):
                If the API key is revoked, clients cannot use it anymore.
                (This cannot be undone).
            expiry_date(datetime):
                Дата окончания действия ключа.
            organization(str):
                Организация.  Связана с моделью Organization через ForeignKey.
            blocked(bool):
                If the API key is blocked, clients cannot use it anymore.
    """
    objects = OrganizationAPIKeyManager()

    organization = models.ForeignKey(
        verbose_name='Идентификатор организации',
        to=Organization,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    blocked = models.BooleanField(
        verbose_name='Временная блокировка ключа',
        default=False,
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "API ключи организации"
        verbose_name_plural = "API ключи организаций"
        db_table = "api_api_keys"
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'name'],
                condition=Q(revoked=False),
                name='unique_organization_APY_Key_name_when_not_revoked',
                violation_error_message='Имя ключа должно быть уникальным'
            )
        ]

    @property
    def is_active(self) -> bool:
        """Возвращает True, если API ключ не заблокирован"""
        return not (
            self.blocked or self.revoked or self.has_expired or
            (self.organization.state != OrganizationStateChoice.ACTIVE)
        )

    def __str__(self):
        return (
            f'{self.organization.name}, '
            f'имя api ключа: {self.name}, '
            f'{"активен" if self.is_active else "заблокирован"}'
        )


class AbstractMessage(models.Model):
    """Сообщение, полученое от заказчика посредством REST API.

         Attributes:
            message(str):
                Текст сообщения о проблеме.  Обязательное поле.
            note(str):
                Примечание к сообщению.  Опциональное поле.
            building(str):
                Здание из которого пришло сообщение.  Обязательное поле.
            system(str):
                Система, в которая требует к себе внимания.  Обязательное поле.
            node(str):
                Конкретный узел системы, на который нужно обратить внимание.  Обязательное поле.
            priority(int):
                Важность сообщения.  Обязательное поле.
    """
    message = models.CharField(max_length=250, verbose_name=_('Сообщение'), blank=False)
    note = models.CharField(max_length=250, verbose_name=_('Примечание'), blank=True)
    building = models.CharField(max_length=250, verbose_name=_('Здание'), blank=False)
    system = models.CharField(max_length=150, verbose_name=_('Система'), blank=False)
    node = models.CharField(max_length=150, verbose_name=_('Узел системы'), blank=False)
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Приоритет'),
        choices=PriorityChoice,
        default=PriorityChoice.NORMAL,
        blank=False,
    )

    class Meta:
        abstract = True


class Message(BaseModel):
    """Сообщение, полученое от заказчика посредством REST API.

         Attributes:
            message(str):
                Текст сообщения о проблеме.  Обязательное поле.
            note(Optional[str]):
                Примечание к сообщению.  Опциональное поле.
            building(str):
                Здание из которого пришло сообщение.  Обязательное поле.
            system(str):
                Система, в которая требует к себе внимания.  Обязательное поле.
            node(str):
                Конкретный узел системы, на который нужно обратить внимание.  Обязательное поле.
            priority(int):
                Важность сообщения.  Обязательное поле.
    """
    message: str = Field(max_length=250)
    note: Optional[str] = Field(max_length=250, default=None)
    building: str = Field(max_length=250)
    system: str = Field(max_length=150)
    node: str = Field(max_length=150)
    priority: PriorityEnum = PriorityEnum.NORMAL


class APIMessage(BaseModel):
    message: Message

