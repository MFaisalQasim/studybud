from django.shortcuts import render, HttpResponse, redirect
from .models import Profile, Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RoomForm
from django.db.models import Q

# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request, 'base/index.html')

@login_required(login_url='login')
def rooms(request):
    # profiles
    profiles = Profile.objects.all()
    # topics
    topics = Topic.objects.all()
    # rooms filter
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(name__icontains=q) |
        Q(desc__icontains=q)
        )
    rooms_count = rooms.count()
    
    context = {'profiles' : profiles, 'rooms' : rooms, 'topics' : topics, 'rooms_count': rooms_count}
    return render(request, 'base/rooms.html', context)

@login_required(login_url='login')
def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = { 'profile': profile }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    context = { 'room': room }
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):

    roomForm = RoomForm()
    if request.method ==  'POST':
        roomForm = RoomForm(request.POST)
        if roomForm.is_valid():
            roomForm.save()
        return redirect("/")
    
    context = { 'roomForm': roomForm }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')    
def updateRoom(request, id):
    
    room = Room.objects.get(id=id)
    roomForm = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed Here')
    if request.method ==  'POST':
        roomForm = RoomForm(request.POST, instance=room)
        if roomForm.is_valid():
            roomForm.save()
        return redirect("/")
    
    context = { 'roomForm': roomForm }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, id):

    room = Room.objects.get(id=id)
    if request.method ==  'POST':
        room.delete()
        return redirect("/")    
    return render(request, 'base/delete.html', {'obj' : room})

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
            messages.error(request,'Sometime Goes Wrong During Register')            
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
            messages.error(request,'User Does Not Exists')
            return redirect('login')

        loginedInUser = authenticate(request,username= username, password= password)
        if loginedInUser is not None:
            login(request,loginedInUser)
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