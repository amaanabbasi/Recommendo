from django import forms
from .models import AppUser, Interest, KeyVal
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class AppUserForm(forms.ModelForm):

    class Meta():
        model = AppUser
        fields = ('user_id', 'profile_pic', 'locale', 'birthyear',
                  'gender', 'location', 'timezone')


class KeyValForm(forms.ModelForm):
    class Meta():
        model=KeyVal
        fields=('container','interest_level')
