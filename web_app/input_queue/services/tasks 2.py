import json
import logging
import uuid
from typing import Any

from celery.app import shared_task
from django.db import transaction

from core.input_channel import InputChannelChoice
from core.output_channel import OutputChannelChoice
from input_queue.models import InputQueue


@shared_task(bind=True)
def input_event_handler(self, db_id: int):
    """Обработчик входящего события"""
    task_id = self.request.id
    task_uuid = uuid.UUID(hex=f'{task_id}')

    with transaction.atomic():
        input_event = InputQueue.objects.get(id=db_id)
        is_first_run = input_event.chain.get("root", None) is None
        if is_first_run:
            run_count = 1
            next_tasks = []
        else:
            run_count = input_event.chain["root"]["count"] + 1
            next_tasks = input_event.chain["root"]["next"]
        InputQueue.objects.filter(pk=db_id).update(
            chain={"root": {"id": task_id, "completed": False, "next": next_tasks, "count": run_count}}
        )

    organization_id = input_event.organization_id
    if organization_id is None:
        # Не можем дальше ничего делать
        logging.error("Нет данных об организации, приславшей сообщение.  Дальнейшая обработка невозможна.")
        pass

    # Считываем фильтры организации
    filters: list[Any] = []

    # Применяем фильтры к сообщению с целью получить списки рассылок
    mailing_lists: dict[OutputChannelChoice: set[Any]] = {}
    for filter in filters:
        # Получаем список рассылки исходя из правила фильтрации
        mailing_list: dict[OutputChannelChoice: set[Any]] = {}

        # Объединяем его с общим списком рассылки
        for channel in mailing_list.keys():
            if channel not in mailing_lists.keys():
                mailing_lists[channel] = mailing_list[channel]
            else:
                mailing_lists[channel] = mailing_lists[channel].union(mailing_list[channel])

    # Проверяем получившийся список и убираем пустые каналы
    for channel in mailing_lists.keys():
        if len(mailing_lists[channel]) == 0:
            del mailing_lists[channel]

    # Проверяем, осталось хоть что нибудь
    if len(mailing_lists) == 0:
        # Берём дефолтный канал и всех абонентов в нём
        mailing_lists = {OutputChannelChoice.EMAIL: ["ove@stinco.net"]}

    logging.info(f'Mailing lists: {mailing_lists}')

    # Формируем задачи для почтампов


    # Отправляем задачи почтампам


    # Делаем отметку о выполнении задачи
    with transaction.atomic():
        dataset = InputQueue.objects.filter(pk=db_id).values_list('chain', flat=True).first()
        dataset["root"]["completed"] = True
        InputQueue.objects.filter(pk=db_id).update(chain=dataset)

    return True

