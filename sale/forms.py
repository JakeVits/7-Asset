from django.contrib.auth.forms import UserCreationForm, User
from .models import Asset
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['owner', 'category', 'name', 'price', 'image', 'address', 'phone_number', 'description']
