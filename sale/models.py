from django.db import models
from django.contrib.auth.forms import User
from django.urls import reverse
from django.core.validators import RegexValidator


class Account(models.Model):
    objects = None
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile = models.ImageField(upload_to='profile', default='profile/default_user.jpg', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.username)


class Asset(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='owner', null=True)
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='stock_image')
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=16)
    address = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('sale:update_asset', kwargs={'pk': self.id})

    def __str__(self):
        return f"{self.owner} owns a {self.name}"

