from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from .forms import RegistrationForm
from .models import Profile, User


# to handle user registration
class Registration(generic.CreateView):
    template_name = 'sale/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('sale:dashboard')
    ''' if inputs are validated '''
    def form_valid(self, form):
        form.save()
        ''' authenticate and login the new user '''
        print(form.get_user())
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        user = self.request.user
        Profile(user_id=User.objects.get(id=user.id)).save()  # create new instance in Profile Table
        self.request.session.set_expiry(7200)


# to handle user login/authentication
def logInUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        ''' to check if input credentials are valid or not '''
        if form.is_valid():
            ''' to restrict admin from accessing the platform '''
            if User.objects.get(username=form.cleaned_data['username']).is_superuser:
                messages.warning(request, 'Admin account is not permitted to access!')
                return redirect('sale:login')
            login(request, form.get_user())
            request.session.set_expiry(7200)
            return redirect('sale:dashboard')
        else:
            messages.warning(request, 'Username or Password is Incorrect!')
            return redirect('sale:login')
    return redirect('login')


# to handle password updates
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password is Updated!')
            return redirect('sale:settings')
        else:
            error_message = [error for error in form.errors]
            message = ''
            for i in error_message:
                message += form.errors[i]
            messages.warning(request, message)
            return redirect('sale:settings')
    return redirect('sale:settings')


# to handle username update
def changeUsername(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        password = request.POST.get('password')
        # authenticate the current user with the input password
        user = authenticate(request, username=str(request.user), password=password)
        if user is not None:
            # to check if new username is in used
            if User.objects.filter(username=new_username):
                messages.info(request, 'This Username is in Used!')
                return redirect('sale:settings')
            current_user = User.objects.get(username=request.user)
            current_user.username = new_username
            current_user.save()
            messages.success(request, 'Username is Updated!')
            return redirect('sale:settings')
        else:
            messages.info(request, 'Password is Incorrect!')
            return redirect('sale:settings')
    return redirect('sale:settings')


# to handle email updates
def changeEmail(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        password = request.POST.get('password')
        # authenticate the current user with the input password
        user = authenticate(request, username=str(request.user), password=password)
        if user is not None:
            if User.objects.filter(email=new_email):
                messages.info(request, 'This Email is in Used!')
                return redirect('sale:settings')
            current_user = User.objects.get(username=request.user)
            current_user.email = new_email
            current_user.save()
            messages.success(request, 'Email is Updated!')
            return redirect('sale:settings')
        else:
            messages.info(request, 'Password is Incorrect!')
            return redirect('sale:settings')
    return redirect('sale:settings')
