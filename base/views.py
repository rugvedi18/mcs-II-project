from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
    context = {'page': page}

    return render(request, template_name, context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration')

    template_name = 'base/login_register.html'
    context = {'form': form}

    return render(request, template_name, context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    template_name = 'base/home.html'
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }

    return render(request, template_name, context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # get all the msgs specific to the above room
    # the message is the Model name and _set.all() is set of msgs
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    template_name = 'base/room.html'
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}

    return render(request, template_name, context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()  # get all the children of a object
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    template_name = 'base/profile.html'
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}

    return render(request, template_name, context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('index')

    template_name = 'base/room_form.html'
    context = {'form': form}

    return render(request, template_name, context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowd here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')

    template_name = 'base/room_form.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowd here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('index')

    template_name = 'base/delete.html'

    return render(request, template_name, {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowd here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('index')

    template_name = 'base/delete.html'

    return render(request, template_name, {'obj': message})
