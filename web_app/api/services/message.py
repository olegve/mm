import json
import logging
from typing import Any

from api.models import APIMessageRawDatagram, Meta, OrganizationAPIKey, MessageMeta, Message
from core.exceptions import InputDataError
from core.input_data_handler import AbstractInputDataHandler


class APIDataHandler(AbstractInputDataHandler):
    """Конвертирует тело API запроса ([POST] /api/message) в объект Message"""

    def _convert_to_message(self, raw_message: Any) -> Message:
        try:
            msg = APIMessageRawDatagram.parse_raw(raw_message)
            return msg.message
        except ValueError as ex:
            raise InputDataError(json.loads(ex.json())) from ex

    def _convert_to_meta(self, raw_meta: Any) -> Meta:
        self._organization = OrganizationAPIKey.org(raw_meta.get('HTTP_X_API_KEY'))
        try:
            meta = Meta(
                organization_id=self._organization.id,
                data=MessageMeta().parse_obj(raw_meta)
            )
            return meta
        except ValueError as ex:
            raise InputDataError(json.loads(ex.json())) from ex
