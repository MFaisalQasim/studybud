from django.urls import path
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