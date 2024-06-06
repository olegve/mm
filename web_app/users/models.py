from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from organizations.models import Organization


class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('Организация'),
        on_delete=models.CASCADE,
        related_name='users',
    )
    phone = models.CharField(
        verbose_name=_('Номер телефона'),
        max_length=20,
        blank=True,
        default=None,
        null=True,
    )
    phone_verified = models.BooleanField(
        verbose_name=_('Номер телефона'),
        default=False,
    )
    is_admin = models.BooleanField(
        verbose_name=_('Администратор организации'),
        default=False,
        help_text=_("Отметьте, если пользователь является администратором в своей организации.")
    )
    REQUIRED_FIELDS = [f'{AbstractUser.EMAIL_FIELD}', "organization_id"]

    class Meta:
        db_table = 'auth_user'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

