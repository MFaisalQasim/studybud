from django.forms import ModelForm
from .models import Room, Messages, User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):    
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']
class RoomForm(ModelForm):    
    class Meta:
        model = Room
        fields = '__all__'
class MessageForm(ModelForm):    
    class Meta:
        model = Messages
        fields = '__all__'

class UserForm(ModelForm):    
    class Meta:
        model =User
        fields = ['username', 'email']