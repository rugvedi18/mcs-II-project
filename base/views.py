from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or password does not exist')

    template_name = 'base/login_register.html'
    context = {}

    return render(request, template_name, context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    template_name = 'base/home.html'
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }

    return render(request, template_name, context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    template_name = 'base/room.html'
    context = {'room': room}

    return render(request, template_name, context)


def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    template_name = 'base/room_form.html'
    context = {'form': form}

    return render(request, template_name, context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')

    template_name = 'base/room_form.html'
    context = {'form': form}
    return render(request, template_name, context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('index')

    template_name = 'base/delete.html'

    return render(request, template_name, {'obj': room})
