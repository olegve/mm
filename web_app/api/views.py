import logging

from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import OrganizationAPIKey
from core.daytime import Daytime, now
from organizations.models import Organization


@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request) -> Response:
    logging.info("PING")
    time: Daytime = now()
    response_data = {
            'ping': 'pong',
            'timestamp': f'{time.timestamp}',
            'time_zone': f'{time.time_zone}'
        }
    """Retrieve a company based on the request API key."""
    sec_key = request.META.get('HTTP_X_API_KEY')
    if sec_key is not None:
        try:
            api_key = OrganizationAPIKey.objects.get_from_key(sec_key)
            organization = Organization.objects.get(api_keys=api_key)
            response_data['organization'] = {
                'name': organization.name,
                'status': organization.status_name(),
            }
            expiry_date = api_key.expiry_date
            if expiry_date:
                response_data['organization']['expiry_date'] = expiry_date
        except Exception as ex:
            response_data['organization'] = {'name': 'unknown'}
    return Response(response_data, status=status.HTTP_200_OK)

