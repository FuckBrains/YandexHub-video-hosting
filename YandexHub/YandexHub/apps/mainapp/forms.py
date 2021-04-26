from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import ModelForm, TextInput, TimeField, Textarea

class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class VideoTextArea(ModelForm):
    class Meta:
        model = Video
        fields = ['description']
        widgets = {
            'description': SummernoteWidget(),
        }

class ArticleTextArea(ModelForm):
    class Meta:
        model = Article
        fields = ['text']
        widgets = {
            'text': SummernoteWidget(),
        }

class CustomUserTextArea(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['description']
        widgets = {
            'description': SummernoteWidget(),
        }