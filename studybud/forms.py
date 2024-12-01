from django.forms import ModelForm
from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import Room, User,Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'pdf_file']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 2}),
        }