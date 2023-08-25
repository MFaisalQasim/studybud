from django.shortcuts import render, HttpResponse
from .models import Profile

# Create your views here.

def index(request):
    profiles = Profile.objects.all()
    context = {
        'profiles' : profiles
        }
    return render(request, 'base/index.html', context)

def home(request):
    return render(request, 'base/home.html')

def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # profile = None
    # for i in profiles:
    #   if i['id'] == int[pk]:
    #       profile == i
    context = { 'profile': profile }
    return render(request, 'base/profile.html', context)