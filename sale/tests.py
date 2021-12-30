from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
# from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login

class UserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='kate', email='kate@gmail.com')
        self.user.set_password('kate123')
        self.user.save()

    def test_registration(self): 
        response = self.client.get(reverse('sale:registration'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/registration.html') 
        self.assertIsNotNone(self.user)      

    def test_login(self):
        user = self.client.login(username='kate', password='kate123')
        self.assertEquals(user, not None)

    def test_sites(self):
        self.test_login()
        response = self.client.get(reverse('sale:dashboard'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/dashboard.html') 
        
    def test_logout(self):
        user = self.client.logout()
        self.assertEqual(user, None)
        response = self.client.get(reverse('sale:dashboard'))
        self.assertEquals(response.status_code, 302)


class AssetTestCase(TestCase):

    def setUp(self):
        user = UserTestCase()
        user.setUp()
        self.client.login(username='kate', password='kate123')
        
    def test_create_asset(self): 
        response = self.client.get(reverse('sale:create_asset'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/new_asset.html') 
        response = self.client.post(reverse('sale:create_asset'), follow=True)
        self.assertContains(response, 'Failed to add stock!')
        self.assertEquals(response.status_code, 200)


