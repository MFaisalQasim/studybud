from django.shortcuts import render, HttpResponse, redirect
from .models import Profile, Room, Topic, Messages, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm, MessageForm, UserForm
# , MyUserCreationForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
 

@login_required(login_url='login')
def index(request):
    return render(request, 'base/index.html')


@login_required(login_url='login')
def rooms(request):

    profiles = User.objects.all()
    topics = Topic.objects.all()
    all_Rooms = Room.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(name__icontains=q) |
        Q(desc__icontains=q)
    )

    recent_activities = Messages.objects.filter(
        Q(room__topic__name__icontains=q)
    ).order_by('-created')

    context = {'profiles': profiles,
               'rooms': rooms, 'topics': topics,
               'recent_activities': recent_activities,
               'all_Rooms': all_Rooms,
               }
    return render(request, 'base/rooms.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all().order_by('-created')
    participants = room.participants.all()
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
               'participants': participants,
               'topics': topics}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def profiles(request):
    profiles = User.objects.all()
    context = {
        'profiles': profiles,
    }
    return render(request, 'base/profiles.html', context)


@login_required(login_url='login')
def profile(request, pk):
    profile = User.objects.get(id=pk)
    rooms = profile.room_set.all().order_by('-created')
    recent_activities = profile.messages_set.all().order_by('-created')
    topics = Topic.objects.all()
    context = {'profile': profile, 'topics': topics,
               'recent_activities': recent_activities,
               'rooms': rooms,
               }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateProfile(request, id):
    user = request.user
    user_form = UserForm(instance=user)
    if request.user != user:
        return HttpResponse('You Are Not Allowed Here')
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user.save()
        return redirect("/")

    context = {
        'user_form': user_form,
        'user': user, }
    return render(request, 'base/user_form.html', context)


@login_required(login_url='login')
def createRoom(request):

    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            desc=request.POST.get('desc'),
        )
        return redirect('/')

    context = {
        'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    room_form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.desc = request.POST.get('desc')
        room.save()
        return redirect("/")

    context = {
        'room_form': room_form, 'topics': topics,
        'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, id):

    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here')

    if request.method == 'POST':
        room.delete()
        return redirect("/")
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def updateMessage(request, id):

    messages = Messages.objects.get(id=id)
    message_form = MessageForm(instance=messages)
    if request.user != messages.user:
        return HttpResponse('You Are Not Allowed Here')
    if request.method == 'POST':
        message_form = MessageForm(request.POST, instance=messages)
        if message_form.is_valid():
            message_form.save()
        return redirect("/room")

    context = {'message_form': message_form}
    return render(request, 'base/message_form.html', context)


@login_required(login_url='login')
def deleteMessage(request, id):

    messages = Messages.objects.get(id=id)
    if request.user != messages.user:
        return HttpResponse('You Are Not Allowed Here')
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
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User Does Not Exists')
            return redirect('login')

        loginedInUser = authenticate(
            request, email=email, password=password)
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
