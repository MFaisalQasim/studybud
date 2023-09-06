"""
URL configuration for studybud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.rooms, name='rooms')
Class-based views
    1. Add an import:  from other_app.views import rooms
    2. Add a URL to urlpatterns:  path('', rooms.as_view(), name='rooms')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('profiles', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('update-profile/<str:id>', views.updateProfile, name='update-profile'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room', views.createRoom, name='create-room'),
    path('update-room/<str:id>', views.updateRoom, name='update-room'),
    path('delete-room/<str:id>', views.deleteRoom, name='delete-room'),
    path('update-message/<str:id>', views.updateMessage, name='update-message'),
    path('delete-message/<str:id>', views.deleteMessage, name='delete-message'),
    path('register', views.registerUser, name='register'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
]