from django.contrib import admin
from .models import Profile, Room, Messages, Topic

# Register your models here.
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Messages)
admin.site.register(Topic)