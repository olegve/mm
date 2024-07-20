import json
import logging

from django.db.models import F
from pydantic import ValidationError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import APIMessageRawDatagram, MessageMeta, OrganizationAPIKey, Meta
from api.permissions import HasOrganizationAPIKey
from api.services import ping_response
from core.input_channel import InputChannelChoice
from core.input_data_handler_fabric import InputDataHandler
from input_queue.models import InputQueue

from input_queue.services.save_message import save_to_input_queue, update_input_queue
from input_queue.services.tasks import input_event_handler


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
    """Получение сообщения от Организации для обработки и пересылке адресатам"""
    input_data = InputDataHandler.make(channel=InputChannelChoice.API_MESSAGE)
    input_data.convert(message=request.body, meta=request.META)
    if not input_data.is_valid:
        logging.error(f'CONVERTER ERROR: {input_data.error}')
        return Response(
            data={"status": "request unprocessable", "validation_error": input_data.error},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    input_data.save()
    task_id = input_data.start_task()
    return Response(data={"status": "message is saved", "next_task_id": f"{task_id}"}, status=status.HTTP_200_OK)

