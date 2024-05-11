from api.models import OrganizationAPIKey
from core.daytime import Daytime, now
from core.organization_state import OrganizationStateChoice
from organizations.models import Organization


def response_data(request):
    time: Daytime = now()
    data = {
        'ping': 'pong',
        'timestamp': f'{time.timestamp}',
        'time_zone': f'{time.time_zone}'
    }
    return data


def organization_data(request):
    data = None
    sec_key = request.META.get('HTTP_X_API_KEY')
    if sec_key is not None:
        try:
            api_key = OrganizationAPIKey.objects.get_from_key(sec_key)
            data = {
                'name': f'{api_key.organization.name}',
                'state': OrganizationStateChoice(api_key.organization.state).label,
            }
            expiry_date = api_key.expiry_date
            if expiry_date:
                data['expiry_date'] = expiry_date
        except Exception as ex:
            data = {'name': 'unknown'}
    return data

