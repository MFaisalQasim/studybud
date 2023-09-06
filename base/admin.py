from django.contrib import admin
from .models import Profile, Room, Messages, Topic, User

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Messages)
admin.site.register(Topic)