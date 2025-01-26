from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import SiteUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = SiteUser
        fields = ['username' , 'email' ]




class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = SiteUser
        fields = ['username' , 'email' ]
