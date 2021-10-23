from django.contrib.auth.forms import UserCreationForm, User
from .models import Asset, Profile
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['owner', 'category', 'name', 'price', 'image', 'description']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_id', 'address', 'phone_number', 'bio', 'image']
