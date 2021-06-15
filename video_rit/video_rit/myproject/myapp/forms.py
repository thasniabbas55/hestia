from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'Description', 'keywords', 'video']


class feedback_Form(forms.Form):
    feedback = forms.CharField(max_length=200)


class Search_form(forms.Form):
    search = forms.CharField(max_length=150)


class Chat_form(forms.Form):
    question = forms.CharField(max_length=50)
