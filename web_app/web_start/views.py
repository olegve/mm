import logging


from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from users.models import User


def index(request):
    users = User.objects.all()
    for user in users:
        logging.info(f'USER: {user.username}')
    context = {"is_authenticated": request.user.is_authenticated}
    return render(request, "index.html", context)

