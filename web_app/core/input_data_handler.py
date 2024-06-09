import json
import logging
import uuid
from abc import abstractmethod
from typing import Optional, Any

from api.models import Message, Meta, APIMessageRawDatagram
from core.exceptions import InputDataError
from input_queue.models import InputQueue
from input_queue.services.tasks import input_event_handler
from organizations.models import Organization


class AbstractInputDataHandler:
    """ Абстрактный класс, конвертер входных данных.

        Основной функционал выполняет метод **convert**, который получает входные данные и преобразует их
        во внутреннее представление.

        Attributes:
            message(Message):
                Полученное (уже преобразованное) сообщение от пользователя.
            extra_data(Any | None):
                Дополнительная информация к сообщению (если есть).
            meta(Meta):
                Метаданные.
            is_valid(bool):
                Показывает, валидность полученых данных.  Если валидных данных нет, то при обращении к
                свойствам **message**, **extra_data** и **meta** выбрасывается исключение.
            error(dict[str, Any]):
                Содержит сообщение об ошибке, если при вызове метода **convert** не удалось привести входные
                данные к необходимому виду.

    """
    def __init__(self):
        self._message: Optional[Message] = None
        self._extra_data: Optional[Any] = None
        self._meta: Optional[Meta] = None
        self._error: dict[str: Any] = {"error": 'unknown'}
        self._is_valid: bool = False
        self._db_id: Optional[int] = None
        self._organization: Optional[Organization] = None

    @property
    def message(self) -> Message:
        """Возвращает входные данные в формате Message, либо выкидывает ошибку"""
        if self.is_valid:
            return self._message
        else:
            raise

    @property
    def extra_data(self) -> Optional[Any]:
        """Возвращает дополнительные данные"""
        if self.is_valid:
            return self._extra_data
        else:
            raise

    @property
    def meta(self) -> Meta:
        """Возвращает входные данные в Meta"""
        if self.is_valid:
            return self._meta
        else:
            raise

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def error(self) -> dict[str, Any]:
        return self._error

    @abstractmethod
    def _convert_to_message(self, raw_message: Any) -> Message:
        """Конвертирует входные данные в Message. Если это невозможно, то выбрасывает исключение"""

    def _convert_to_extra_data(self, raw_extra: Any) -> Optional[Any]:
        """Конвертирует входные данные в Message. Если это невозможно, то выбрасывает исключение"""
        return None

    @abstractmethod
    def _convert_to_meta(self, raw_meta: Any) -> Meta:
        """Конвертирует входные данные в Message. Если это невозможно, то выбрасывает исключение"""

    def convert(self, message: Any, meta: Any, extra: Optional[Any] = None) -> None:
        """ Конвертирует входные данные во внутренние типы данных объекта.
            Если не получается, то устанавливает is_valid в False и записывает сообщение
            об ошибке в свойство error.
        """
        try:
            self._message = self._convert_to_message(message)
            self._extra_data = self._convert_to_extra_data(extra)
            self._meta = self._convert_to_meta(meta)
            self._error = {}
            self._is_valid = True
        except Exception as ex:
            self._message = None
            self._extra_data = None
            self._meta = None
            try:
                self._error = {"error": json.loads((f'{ex}').replace("\'", "\""))}
            except Exception as json_ex:
                self._error = {"error": f"{ex}"}
            self._is_valid = False

    def save(self) -> int:
        """Создаёт запись в таблице базы данных.
            :return: id созданой записи в таблице модели InputQueue
        """
        if not self._db_id:
            message_for_save = APIMessageRawDatagram(message=self.message)
            message_for_save = json.loads(message_for_save.model_dump_json())
            meta_for_save = json.loads(self.meta.model_dump_json())
            table_row = InputQueue.objects.create(
                organization=self._organization,
                message=message_for_save,
                meta=meta_for_save
            )
            self._db_id = table_row.id
        return self._db_id

    def start_task(self) -> str:
        """Запускает задачу обработки входящего сообщения"""
        if not self.is_valid:
            raise
        if self._db_id:
            task_priority = self.message.priority.value * 2
            return input_event_handler.apply_async(
                args=(self._db_id,),
                priority=task_priority,
                ignore_result=True,

            )
        else:
            raise InputDataError('Входящее сообщение пока не сохранено в базе данных.')

