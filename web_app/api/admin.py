import logging
from django.contrib import admin

from rest_framework_api_key.admin import APIKeyModelAdmin

from api.api_key import APIKeyFilter
from api.models import OrganizationAPIKey


@admin.register(OrganizationAPIKey)
class OrganizationAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = (
        "organization",
        "prefix",
        "name",
        "created",
        "expiry_date",
        "_has_expired",
        "revoked",
        "blocked",
        "is_active",
    )
    list_filter = ("created", APIKeyFilter, )
    search_fields = ("name", "prefix", "organization__id", "organization__name",)

    def is_active(self, instance):
        """
        Shadow function
        Сделана для того, чтобы свойство (@property) is_active модели показывало как родные поля boolean типа,
        т.е. красивой пиктограммой, а не True/False.
        """
        return instance.is_active

    is_active.boolean = True



