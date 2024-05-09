import logging
from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

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
        "is_active"
    )
    list_filter = ("created",)
    search_fields = ("name", "prefix")



