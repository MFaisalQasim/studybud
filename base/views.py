from django.shortcuts import render, HttpResponse, redirect
from .models import Profile, Room, Topic, Messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RoomForm, MessageForm
from django.db.models import Q


@login_required(login_url='login')
def index(request):
    return render(request, 'base/index.html')


@login_required(login_url='login')
def rooms(request):

    # profiles
    profiles = User.objects.all()
    # profiles_count = profiles.count()

    # topics
    topics = Topic.objects.all()

    # rooms
    all_Rooms = Room.objects.all()
    # all_Rooms_count = all_Rooms.count()

    # rooms filter
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(name__icontains=q) |
        Q(desc__icontains=q)
    )
    # rooms_count = rooms.count()

    # recent_activities
    recent_activities = Messages.objects.filter(
        Q(room__topic__name__icontains=q)
    ).order_by('-created')

    # recent_activities_count = recent_activities.count()

    context = {'profiles': profiles,
               # 'profiles_count': profiles_count,
               'rooms': rooms, 'topics': topics,
               #  'rooms_count': rooms_count,
               'recent_activities': recent_activities,
               #  'recent_activities_count': recent_activities_count,
               'all_Rooms': all_Rooms,
               #  'all_Rooms_count' : all_Rooms_count
               }
    return render(request, 'base/rooms.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all().order_by('-created')
    # room_messages_count = room_messages.count()
    participants = room.participants.all()
    # participants_count = participants.count()
    topics = Topic.objects.all()
    if request.method == 'POST':
        message = Messages.objects.create(
            room=room,
            user=request.user,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               #  'room_messages_count': room_messages_count,
               'participants': participants,
               #  'participants_count': participants_count,
               'topics': topics}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def profile(request, pk):
    profile = User.objects.get(id=pk)
    rooms = profile.room_set.all().order_by('-created')
    recent_activities = profile.messages_set.all().order_by('-created')
    # recent_activities_count = recent_activities.count()
    topics = Topic.objects.all()
    context = {'profile': profile, 'topics': topics,
                  'recent_activities': recent_activities,
               #  'recent_activities_count': recent_activities_count,
               'rooms': rooms,
               }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def profiles(request):
    profiles = User.objects.all()
    context = {'profiles': profiles,
               }
    return render(request, 'base/profiles.html', context)


@login_required(login_url='login')
def createRoom(request):

    room_form = RoomForm()
    if request.method == 'POST':
        room_form = RoomForm(request.POST)
        if room_form.is_valid():
            room_form.save()
        return redirect("/")

    context = {'room_form': room_form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, id):

    room = Room.objects.get(id=id)
    room_form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here')
    if request.method == 'POST':
        room_form = RoomForm(request.POST, instance=room)
        if room_form.is_valid():
            room_form.save()
        return redirect("/")

    context = {'room_form': room_form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateMessage(request, id):

    message = Messages.objects.get(id=id)
    message_form = MessageForm(instance=message)
    if request.user != message.user:
        return HttpResponse('You Are Not Allowed Here')
    if request.method == 'POST':
        message_form = MessageForm(request.POST, instance=message)
        if message_form.is_valid():
            message_form.save()
        return redirect("/room")

    context = {'message_form': message_form}
    return render(request, 'base/message_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, id):

    room = Room.objects.get(id=id)
    if request.method == 'POST':
        room.delete()
        return redirect("/")
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, id):

    messages = Messages.objects.get(id=id)
    if request.method == 'POST':
        messages.delete()
        return redirect("/")
    return render(request, 'base/delete.html', {'obj': messages})


def registerUser(request):

    regiterUserFrom = UserCreationForm()
    if request.method == 'POST':
        regiterUserFrom = UserCreationForm(request.POST)
        if regiterUserFrom.is_valid():
            user = regiterUserFrom.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('rooms')
        else:
            messages.error(request, 'Sometime Goes Wrong During Register')
    context = {'regiterUserFrom': regiterUserFrom}
    return render(request, 'guest/login.html', context)


def loginUser(request):

    page = 'login'
    # if User.is_authenticated:
    #     return redirect('rooms')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exists')
            return redirect('login')

        loginedInUser = authenticate(
            request, username=username, password=password)
        if loginedInUser is not None:
            login(request, loginedInUser)
            return redirect('rooms')
        else:
            messages.error('User`s Credential Are Not Valid')
            return redirect('login')
    context = {'page': page}
    return render(request, 'guest/login.html', context)


@login_required(login_url='login')
def logoutUser(request):

    logout(request)
    return redirect('login')
