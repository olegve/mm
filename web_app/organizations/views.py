from django.shortcuts import render
from rest_framework import viewsets

from api.permissions import HasOrganizationAPIKey
from organizations.models import Organization
from organizations.serializers import OrganizationSerializer


class OrganizationsViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [HasOrganizationAPIKey]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
