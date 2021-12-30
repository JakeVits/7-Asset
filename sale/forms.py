from django.contrib.auth.forms import UserCreationForm, User
from .models import Asset, Profile
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type': 'email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AssetForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Asset-Name'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        'type': 'number',
        'placeholder': 'Price',
        'min': 1,
        'max': 99999999,
    }))

    class Meta:
        model = Asset
        fields = ['owner', 'category', 'name', 'price', 'image', 'description']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_id', 'address', 'phone_number', 'bio', 'image']
