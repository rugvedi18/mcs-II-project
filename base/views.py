from django.shortcuts import render
from .models import Room
# Create your views here.


def home(request):
    rooms = Room.objects.all()
    template_name = 'base/home.html'
    context = {'rooms': rooms}

    return render(request, template_name, context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    template_name = 'base/room.html'
    context = {'room': room}

    return render(request, template_name, context)
