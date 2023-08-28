from django.shortcuts import render, HttpResponse, redirect
from .models import Profile, Room, Topic
from django.contrib.auth.models import User
from .forms import RoomForm
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request, 'base/index.html')

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
    
    context = {'profiles' : profiles, 'rooms' : rooms, 'topics' : topics}
    return render(request, 'base/rooms.html', context)

def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = { 'profile': profile }
    return render(request, 'base/profile.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = { 'room': room }
    return render(request, 'base/room.html', context)
    
def createRoom(request):
    roomForm = RoomForm()
    if request.method ==  'POST':
        roomForm = RoomForm(request.POST)
        if roomForm.is_valid():
            roomForm.save()
        return redirect("/")
    
    context = { 'roomForm': roomForm }
    return render(request, 'base/room_form.html', context)
    
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    roomForm = RoomForm(instance=room)

    if request.method ==  'POST':
        roomForm = RoomForm(request.POST, instance=room)
        if roomForm.is_valid():
            roomForm.save()
        return redirect("/")
    
    context = { 'roomForm': roomForm }
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, id):

    room = Room.objects.get(id=id)
    if request.method ==  'POST':
        room.delete()
        return redirect("/")
    
    return render(request, 'base/delete.html', {'obj' : room})