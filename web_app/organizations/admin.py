from django.forms import BaseInlineFormSet
from django.utils.translation import gettext as _
from django.contrib import admin

from organizations.models import Organization
from users.models import User


class UserInline(admin.TabularInline):
    model = User
    classes = ('collapse',)
    extra = 0
    fields = ('last_name', 'first_name', 'email', 'is_admin')
    readonly_fields = ('last_name', 'first_name', 'email', 'is_admin')
    ordering = ('last_name', 'first_name')
    show_change_link = True
    can_delete = False


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name', 'ИНН', 'state',)
    list_display_links = ('name', 'ИНН')
    ordering = ('name', )
    list_filter = ("state", )
    search_fields = ("name", "id")
    inlines = (UserInline, )
    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'state')
            }
        ),
    )

    def ИНН(self, obj: Organization) -> str:
        return obj.id[0:4] + " " + obj.id[4:8] + " " + obj.id[8:12]

