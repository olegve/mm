import logging
import uuid

from django.core import exceptions


from api.models import APIMessageRawDatagram, MessageMeta
from input_queue.models import InputQueue


def save_to_input_queue(message: APIMessageRawDatagram, meta: MessageMeta) -> int:
    """Создаёт запись в таблице базы данных.
        :param message: пришедшее через API сообщение
        :param meta: дополнительные данные к пришедшему сообщению
        :return: id созданой записи в таблице
    """
    element = InputQueue.objects.create(message=message.model_dump_json(), meta=meta.model_dump_json())
    return element.id


def update_input_queue(db_id: int, task_id: str) -> None:
    """Вписывает в существующую запись с id = db_id номер (uuid) задачи, которая обрабатывает эту строку в базе данных
        :param db_id: id строки таблицы базы данных, которая обрабатывается ассинхронной задачей
        :param task_id: uuid задачи, которая обрабатывает строку базы данных с id = db_id
    """
    task_uuid = uuid.UUID(hex=f'{task_id}')
    InputQueue.objects.select_for_update().filter(pk=db_id).update(next_task=task_uuid)

