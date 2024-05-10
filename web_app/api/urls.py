from django.urls import path, include

from api.views import ping
from web_app.urls import router

app_name = "api"

urlpatterns = [
    path('', include(router.urls)),
    path("ping/", ping, name='ping'),
]
