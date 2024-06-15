import logging


from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from users.models import User


def index(request):
    context = {"user": request.user}
    return render(request, "index.html", context)


def test(request):
    context = {"user": request.user, "title": "Тестовая страница"}
    return render(request, "base.html", context)
