import json
import logging

from pydantic import ValidationError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import APIMessageRawDatagram, MessageMeta, OrganizationAPIKey
from api.permissions import HasOrganizationAPIKey
from api.services import ping_response
from input_queue.services.save_message import save_to_input_queue, update_input_queue
from input_queue.services.tasks import received_messages_handler
from web_app.celery import debug_task


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
        meta.REMOTE_ORGANIZATION_ID = OrganizationAPIKey.org_id(request.META.get('HTTP_X_API_KEY'))
    except ValidationError as ex:
        return Response(
            data={"status": "request unprocessable", "validation_error": json.loads(ex.json())},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    # Запись сообщения в базу денных и постановка задачи на дальнейшую обработку.
    db_id = save_to_input_queue(message=msg, meta=meta)
    task_id = received_messages_handler.delay(db_id=db_id)
    update_input_queue(db_id=db_id, task_id=task_id)
    return Response(
        data={"status": "message is saved", "task_id": f"{task_id}"},
        status=status.HTTP_200_OK
    )
