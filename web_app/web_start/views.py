from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    context = {"is_authenticated": request.user.is_authenticated}
    return render(request, "index.html", context)

