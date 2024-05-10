import logging
from datetime import timezone, datetime

from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from rest_framework_api_key.models import BaseAPIKeyManager

from core.organization_state import ACTIVE


class OrganizationAPIKeyManager(BaseAPIKeyManager):
    """
    Для того, чтобы выполнить свою логику по доступу к API ключам, делаем свой Dgsngo model manager.
    В модель, наследуемую от AbstractAPIKey добавляем строку:
    objects = OrganizationAPIKeyManager().
    """
    def get_usable_keys(self):
        """Убираем из выдачи заблокированые ключи и неактивные компании."""
        return super().get_usable_keys().filter(blocked=False, organization__state=ACTIVE)


class APIKeyFilter(SimpleListFilter):
    """
    This filter is being used in django admin panel in profile model.
    """
    title = 'Состояние API ключей'
    parameter_name = 'is_active_key'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value for the option that will
        appear in the URL query. The second element is the human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('active', 'Активны'),
            ('not_active', 'Заблокированы')
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query string and retrievable via self.value().
        """
        if not self.value():
            return queryset
        filter_queryset = (
                Q(revoked=False) & Q(blocked=False) & Q(organization__state=ACTIVE) &
                (Q(expiry_date__isnull=True) | Q(expiry_date__gte=datetime.now().astimezone()))
        )
        if self.value().lower() == 'active':
            return queryset.filter(filter_queryset)
        elif self.value().lower() == 'not_active':
            return queryset.filter().exclude(filter_queryset)
