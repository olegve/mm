import logging


from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from users.models import User


def index(request):
    base_template = "base_messages_management.html" if request.user.is_authenticated else "base_overview_system.html"
    context = {"base": base_template, "user": request.user, "title": "Тестовая страница"}
    return render(request, "index.html", context)


def test(request):
    base_template = "base_messages_management.html" if request.user.is_authenticated else "base_overview_system.html"
    context = {"base": base_template, "user": request.user, "title": "Тестовая страница"}
    return render(request, "messages_management.html", context)
