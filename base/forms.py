from django.forms import ModelForm
from .models import Room,Messages

class RoomForm(ModelForm):    
    class Meta:
        model = Room
        fields = '__all__'
class MessageForm(ModelForm):    
    class Meta:
        model = Messages
        fields = '__all__'

