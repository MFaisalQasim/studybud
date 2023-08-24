from django.shortcuts import render, HttpResponse

# Create your views here.
profiles = [
    {'id':1 , 'name':'faisal' },
    {'id':2 , 'name':'zahid' },
    {'id':3 , 'name':'tayyab' },
]

def index(request):
    # return HttpResponse("hi there this is faisal") 
    context = {
        'profiles' : profiles
        }
    return render(request, 'base/index.html', context)

def home(request):
    return render(request, 'base/home.html')

def room(request):
    return render(request, 'base/room.html')