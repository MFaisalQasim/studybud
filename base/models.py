from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

    name = models.CharField(("name"), max_length=50)
    email = models.EmailField(("email"), max_length=254)
    about =  models.TextField(("about"), null=True, blank=True)
    created = models.DateTimeField(("created"), auto_now_add=True)
    updated = models.DateTimeField(("updated"), auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    

class Topic(models.Model):

    name = models.CharField(("name"), max_length=100)
    created = models.DateTimeField(("created"), auto_now_add=True)
    updated = models.DateTimeField(("updated"), auto_now=True)
    

    def __str__(self):
        return self.name
    
class Room(models.Model):

    host = models.ForeignKey(User, verbose_name=("host"), on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, verbose_name=("topic"), on_delete=models.SET_NULL, null=True)
    name = models.CharField(("name"), max_length=50)
    participants = models.ManyToManyField(User, related_name='participants')
    desc =  models.TextField(("desc"), null=True, blank=True)
    created = models.DateTimeField(("created"), auto_now_add=True)
    updated = models.DateTimeField(("updated"), auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.name

class Messages(models.Model):

    user = models.ForeignKey(User, verbose_name=("user"), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name=("room"), on_delete=models.CASCADE)
    body =  models.TextField(("body"))
    created = models.DateTimeField(("created"), auto_now_add=True)
    updated = models.DateTimeField(("updated"), auto_now=True)

    def __str__(self):
        return self.body[0:25]
        # return self.id