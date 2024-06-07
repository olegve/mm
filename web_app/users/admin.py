from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('organization', 'last_name', 'first_name', 'username', 'email', 'is_admin')
    list_display_links = ('last_name', 'first_name','username',)
    search_fields = ('organization__name', 'organization__id', 'last_name', 'first_name', 'email', 'username', )
    ordering = ('organization', 'last_name', 'first_name', )
    list_filter = ("is_admin", "is_superuser", )

    fieldsets = (
        (None, {
                'fields': ('username', 'password')
            }
        ),
        (_('Personal info'), {
                'fields': ('last_name', 'first_name', 'email', 'organization')
            }
        ),
        (_('Permissions'), {
                'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
        (_('Important dates'), {
                'fields': ('last_login', 'date_joined')
            }
        ),
    )


admin.site.register(User, CustomUserAdmin)
