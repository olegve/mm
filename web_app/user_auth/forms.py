import logging

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django import forms

from allauth.account.forms import SignupForm

from core.organization_id import is_inn_valid
from organizations.models import Organization


def inn_validator(id: str):
    if not is_inn_valid(id):
        raise ValidationError(_("Organization ID is invalid."))


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label=_('Имя'),
        widget=forms.TextInput(attrs={"placeholder": _("Имя")}),
    )
    last_name = forms.CharField(
        max_length=30,
        label=_('Фамилия'),
        widget=forms.TextInput(attrs={"placeholder": _("Фамилия")}),
    )
    organization_name = forms.CharField(
        label=_("Организация"),
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("Организация")}),
    )
    organization_id = forms.CharField(
        label=_('ИНН'),
        max_length=12,
        min_length=10,
        required=True,
        validators=[inn_validator],
        widget=forms.TextInput(attrs={"placeholder": _("ИНН")}),
    )

    def clean_organization_id(self) -> str:
        organization_id = self.cleaned_data.get('organization_id')
        if Organization.objects.filter(id=organization_id).exists():
            raise ValidationError(_(
                "Организация с этим ИНН уже существует.  Обратитесь к администратору Вашей организации."
            ))
        return organization_id

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_admin = True
        user.save()
        return user

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super().save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
