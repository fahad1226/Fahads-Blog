from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdate(forms.ModelForm):

        email = forms.EmailField()

        class Meta:
            model = User
            fields = ['username','email','first_name','last_name']

class ProfileUpdate(forms.ModelForm):
    nick_name = forms.CharField(max_length=150)
    public_info = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Profile
        fields = ['image','nick_name','public_info']
