from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import OrganizationAPIKey


class HasOrganizationAPIKey(BaseHasAPIKey):
    """Ограничивает доступ только ьем запросам, у которых есть API ключ в заголовке"""
    model = OrganizationAPIKey

