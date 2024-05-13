from django.contrib.postgres.indexes import GinIndex
# from django.contrib.postgres.fields.jsonb import JSONField
from django.utils.translation import gettext as _
from django.db import models

from core.input_channel import InputChannelChoice


class InputQueue(models.Model):
    """Список входящих сообщений

        Attributes:
            message(json):
                Пришедшее в приёмный канал связи необработаное сообщение.
            meta(json):
                Дополнительные данные о сообщении.
            created(datetime):
                Время приёма сообщения во входящий канал.
            channel(int):
                Канал связи, по которому пришло сообщение.
            next_task(UUID):
                Идентификатор фоновой задачи, которая разбирает сообщение и ставит его в очереди доставки потребителям.
            task_completed(bool):
                Указывает, было ли обработано поступившее сообщение и поставлено ли оно в очереди доставки потребителям.
    """
    message = models.JSONField(
        verbose_name=_('Сообщение'),
        blank=False,

    )
    meta = models.JSONField(
        verbose_name=_('Метаданные'),
        blank=False,
    )
    created = models.DateTimeField(
        verbose_name=_('Время создания'),
        blank=False,
        auto_now_add=True
    )
    channel = models.PositiveSmallIntegerField(
        verbose_name=_('Канал'),
        blank=False,
        choices=InputChannelChoice,
        default=InputChannelChoice.API_MESSAGE,

    )
    next_task = models.UUIDField(
        verbose_name=_('Номер задачи'),
        blank=True,
        null=True,
        db_index=True,

    )
    task_completed = models.BooleanField(
        verbose_name=_('Обработано'),
        blank=False,
        default=False,
    )

    class Meta:
        indexes = [GinIndex(name='JSONGinIndex', fields=['message', 'meta'])]


