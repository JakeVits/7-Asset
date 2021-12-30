from django.db import models
from django.contrib.auth.forms import User
from django.urls import reverse
from django.core.validators import RegexValidator


class Profile(models.Model):
    objects = None
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{8,15}$")], max_length=16, null=True)
    bio = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='profile', default='profile/default_user.jpg', null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user_id}"


class Asset(models.Model):
    objects = None
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_owner', null=True)
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image = models.ImageField(upload_to='asset_image')
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    interested_user = models.ManyToManyField(User, related_name='user', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('sale:update_asset', kwargs={'pk': self.id})

    def __str__(self):
        return f"{self.owner} owns a {self.name}"


class Notification(models.Model):
    objects = None
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='assetID', null=True)
    asset_owner = models.CharField(max_length=20, null=True)
    asset_name = models.CharField(max_length=20, null=True)
    interested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interested_user', null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.interested_user} is interested in the asset on {self.date}"


# class Interest(models.Model):
#     objects = None
#     asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='asset_id')
#     interested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
#     total_interest = models.BigIntegerField(default=0)
#
#     def __str__(self):
#         return f"{self.asset_id} has {self.total_interest} interests"
