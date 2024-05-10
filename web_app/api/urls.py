from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ping


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path("ping/", ping, name="ping"),
]

