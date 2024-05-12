import json
import logging

from pydantic import ValidationError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import APIMessageRawDatagram, MessageMeta
from api.permissions import HasOrganizationAPIKey

from api.services import ping_response
from api.services.message import received_messages_handler
from input_queue.services.save_message import save_to_input_queue, update_input_queue


@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request) -> Response:
    """Endpoint, доступный всем."""
    response_data = ping_response.response_data(request)
    """Retrieve a company based on the request API key."""
    organization_data = ping_response.organization_data(request)
    if organization_data:
        response_data["organization"] = organization_data
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([HasOrganizationAPIKey])
def message(request) -> Response:
    # Валидация сообщения
    try:
        msg = APIMessageRawDatagram.parse_raw(request.body)
        meta = MessageMeta().parse_obj(request.META)
    except ValidationError as ex:
        return Response(
            data={"status": "request unprocessable", "validation_error": json.loads(ex.json())},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    # Запись сообщения в базу денных и постановка задачи на дальнейшую обработку.
    id = save_to_input_queue(message=msg, meta=meta)
    task_id = received_messages_handler(db_id=id)
    update_input_queue(db_id=id, task_id=task_id)

    return Response(
        data={"status": "message is saved", "task_id": f'{task_id}'},
        status=status.HTTP_200_OK
    )
