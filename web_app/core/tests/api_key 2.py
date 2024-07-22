import logging
import random
from typing import NamedTuple

from api.models import OrganizationAPIKey
from core.organization_state import OrganizationStateEnum
from core.tests.organization import random_organization_id
from organizations.models import Organization


class APIKey(NamedTuple):
    organization_id: str
    organization_name: str
    api_key_name: str
    api_key_instance: OrganizationAPIKey
    key: str


def get_api_key_for_organization(name: str, id: None | str = None) -> APIKey:
    api_key_name = f"{name}-key-test-service"
    organization = Organization.objects.create(name=name, id=id if id else random_organization_id())
    api_key, key = OrganizationAPIKey.objects.create_key(name=api_key_name, organization=organization)
    return APIKey(
        organization_id=organization.id,
        organization_name=name,
        api_key_name=api_key_name,
        api_key_instance=api_key,
        key=key
    )


def get_random_blocked_organization_state() -> OrganizationStateEnum:
    ls = [
        OrganizationStateEnum.BLOCKED,
        OrganizationStateEnum.PARTIAL,
        OrganizationStateEnum.ARCHIVE,
    ]
    # Тщательно перемешиваем список
    random.shuffle(ls)
    # Извлекаем из списка произвольное значений
    random_state = OrganizationStateEnum(random.choice(ls))
    return random_state


def get_api_key_for_blocked_organization(name: str, id: None | str = None) -> APIKey:
    api_key = get_api_key_for_organization(name, id)
    organization = Organization.objects.get(id=api_key.organization_id)
    state = get_random_blocked_organization_state()
    organization.state = state
    organization.save()
    api_key.api_key_instance.refresh_from_db()
    return api_key
