from django.shortcuts import render
from .models import Room
# Create your views here.


def home(request):
    template_name = 'base/home.html'
    context = {}
    return render(request, template_name, context)


def room(request, id):
    template_name = 'base/room.html'
    context = {}
    return render(request, template_name, context)
