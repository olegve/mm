from django.utils.translation import gettext as _
from django.contrib import admin

from organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'ИНН', 'state',)
    list_display_links = ('name', 'ИНН')
    ordering = ('name', )

    list_filter = ("state", )
    search_fields = ("name", "id")

    def ИНН(self, obj: Organization) -> str:
        return obj.id[0:4] + " " + obj.id[4:8] + " " + obj.id[8:12]


