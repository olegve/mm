import logging

from allauth.account.adapter import DefaultAccountAdapter

from organizations.models import Organization


class AccountAdapter(DefaultAccountAdapter):
    def save_organization(self, request) -> Organization:
        id = request.POST.get('organization_id')
        name = request.POST.get('organization_name')
        try:
            organization = Organization.objects.create(id=id, name=name)
        except Exception as e:
            logging.error(e)
            raise e
        return organization

    def new_user(self, request):
        """
        Instantiates a new User instance.
        """
        user = super().new_user(request)
        organization = self.save_organization(request)
        user.organization = organization
        logging.warning(f"Organization: {organization}, User is {user}")
        return user



