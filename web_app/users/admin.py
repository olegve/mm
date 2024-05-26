from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    readonly_fields = ('organisation',)


admin.site.register(User, CustomUserAdmin)
