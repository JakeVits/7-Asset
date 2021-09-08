from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from .forms import RegistrationForm
from .models import Account, User


# to handle user registration
class Registration(generic.CreateView):
    template_name = 'sale/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('sale:dashboard')
    ''' if inputs are validated '''
    def form_valid(self, form):
        valid = super(Registration, self).form_valid(form)
        user = User.objects.get(username=form.cleaned_data['username'])
        ''' create new user object '''
        username = Account(username=user)
        username.save()
        ''' authenticate and login the new user '''
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
            self.request.session.set_expiry(3600)
            return valid
        else:
            messages.warning(self.request, 'Invalid Authentication!')
            return super().form_invalid(form)


# to handle user login/authentication
def logInUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        ''' to check if input credentials are valid or not '''
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                request.session.set_expiry(3600)
                return redirect('sale:dashboard')
            return redirect('login')
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
            messages.success(request, 'Password is Successfully Changed!')
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
        user = authenticate(request, username=request.user, password=password)
        if user is not None:
            # check if new username is in used
            if User.objects.filter(username=new_username):
                messages.info(request, 'This Username is in Used!')
                return redirect('sale:settings')
            current_user = User.objects.get(username=request.user)
            current_user.username = new_username
            current_user.save()
            messages.success(request, 'Username is Successfully Changed!')
            return redirect('sale:settings')
        else:
            messages.warning(request, 'Password is Incorrect!')
            return redirect('sale:settings')
    return redirect('sale:settings')


# to handle email updates
def changeEmail(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        password = request.POST.get('password')
        # authenticate the current user with the input password
        user = authenticate(request, username=request.user, password=password)
        if user is not None:
            if User.objects.filter(email=new_email):
                messages.info(request, 'This Email is in Used!')
                return redirect('accounts/password_change/')
            current_user = User.objects.get(username=request.user)
            current_user.email = new_email
            current_user.save()
            messages.success(request, 'Email is Successfully Changed!')
            return redirect('sale:settings')
        else:
            messages.warning(request, '* Password you entered was not correct!')
            return redirect('sale:settings')
    return redirect('sale:settings')
