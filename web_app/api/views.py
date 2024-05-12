import json
import logging

from pydantic import ValidationError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import APIMessage

from api.services import ping_response


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
@permission_classes([AllowAny])
def message(request) -> Response:
    try:
        msg = APIMessage.parse_raw(request.body)
    except ValidationError as ex:
        return Response(
            data={"status": "request unprocessable", "validation_error": json.loads(ex.json())},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return Response(
        data={"status": "message is saved", "task_id": f'{"123-123-456-789"}'},
        status=status.HTTP_200_OK
    )
