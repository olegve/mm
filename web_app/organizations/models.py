from typing import NamedTuple
from django.db import models

from core.organization_state import OrganizationStateChoice


class Organization(models.Model):
    """Организации, использующие сервис пересылки сообщений.

        Attributes:
            id(str):
                Уникальный идентификатор организации, например, для России - ИНН.
                Установлены ограничения по длине и уникальности.
                Поле являтся первичным ключом таблицы
            name(str):
                Название организации.
                Установлены ограничения по длине.
                Обязателбно для заполнения.
            state(str):
                Состояние (статус) организации в системе.
                Поле обязательно для заполнения.  Состояние по умолчанию - ACTIVE
    """



    id = models.CharField(
        verbose_name='Идентификатор',
        max_length=50,
        db_index=True,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name='Органицация',
        max_length=200,
        blank=False,
        null=False,
    )
    state = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=OrganizationStateChoice,
        default=OrganizationStateChoice.ACTIVE,
    )

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ("name",)
        # constraints = ()

    def status_name(self) -> str:
        # return next((x[1] for x in STATE_CHOICES if x[0] == self.state), 'Состояние неопределено')
        return str(OrganizationStateChoice(self.state).label)

    def __str__(self):
        return f'{self.name}, id: {self.id} ({self.status_name()})'


class OrganizationDetails(models.Model):
    """Различные реквизиты организации.

        Attributes:
            organization(str):
                Организация.  Связана с моделью Organization через OneToOneField.
            address(str):
                Адрес организации.
                Установлены ограничения по длине.
            phone(str):
                Телефон для связи с организацией.
                Установлены ограничения по длине.
            email(str):
                Адрес электронной почты организации.
                Поле обязательно для заполнения.
            email_verified(bool):
                Статус проверки электронной почты.
                По умолчанию = False, т.е. проверка подлиности не пройдена.
                Поле обязательно для заполнения.
        """

    organization = models.OneToOneField(
        verbose_name='Идентификатор организации',
        to=Organization,
        on_delete=models.CASCADE,
        related_name="details"
    )
    address = models.CharField(
        verbose_name='Фактический адрес',
        max_length=255,
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=20,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        blank=False,
        null=False,
    )
    email_verified = models.BooleanField(
        verbose_name='Статус верефикации электронной почты',
        default=False,
        blank=False,
    )

    class Meta:
        verbose_name = "Реквизиты организации"
        verbose_name_plural = "Реквизиты рганизаций"
        # ordering = ("name",)
        # constraints = ()

    def __str__(self):
        return (
            f'{self.organization.name}, '
            f'почта: {self.email if self.email_verified else "не верифицирована"}'
            f''
        )