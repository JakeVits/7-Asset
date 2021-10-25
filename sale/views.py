from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy, reverse
from .models import User, Asset, Profile, Notification
from .forms import AssetForm, ProfileForm
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
import json


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'sale/dashboard.html'


class CreateAssetView(LoginRequiredMixin, generic.CreateView):
    template_name = 'sale/new_asset.html'
    form_class = AssetForm
    success_url = reverse_lazy('sale:new_asset')

    def form_valid(self, form):
        asset = form.save(commit=False)
        asset_name = form.cleaned_data['name'].title().strip()
        asset.name = asset_name
        form.save()
        messages.success(self.request, 'Asset has been added!')
        print('==========================', self.request.FILES.get('image'), '================================')
        return redirect('sale:create_asset')

    def form_invalid(self, form):
        print('==========================', 'File is not valid', '================================')
        print('==========================', self.request.FILES.get('image'), '================================')
        messages.warning(self.request, 'Failed to add stock!')
        return redirect('sale:create_asset')


class InventoryView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/inventory.html'
    context_object_name = 'asset_list'

    def post(self, *args):
        asset_id = self.request.POST.getlist('checkbox')  # get checked box value to delete asset
        if asset_id:
            for asset_id in asset_id:
                Asset.objects.get(id=asset_id).delete()
        else:
            Asset.objects.filter(owner=self.request.user).delete()
        return redirect('sale:inventory')

    def get_queryset(self):
        asset_name = self.request.GET.get('asset_name')
        if asset_name:
            return Asset.objects.filter(owner=self.request.user, name__icontains=asset_name).order_by('-created_at')
        return Asset.objects.filter(owner=self.request.user).order_by('-created_at')


class AssetDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sale/asset_details.html'
    model = Asset
    context_object_name = 'asset'

    def get_object(self):
        return get_object_or_404(Asset, id=self.kwargs.get('pk'))


class UpdateAssetView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'sale/update_asset.html'
    form_class = AssetForm
    model = Asset
    context_object_name = 'update_asset'
    ''' function to authorize user '''

    def get(self, *args, pk):
        if authorizeUser(self.request, pk):
            return render(self.request, self.template_name,
                          {'update_asset': Asset.objects.get(id=self.kwargs.get('pk'))})
        return redirect('sale:dashboard')

    def form_valid(self, form):
        asset = form.save(commit=False)
        asset.name = form.cleaned_data['name'].title().strip()
        form.save()
        messages.success(self.request, 'Updated Successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Failed to update stock!')
        return redirect('sale:update_asset', pk=self.kwargs.get('pk'))


class DeleteAssetView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'sale/inventory.html'
    success_url = reverse_lazy('sale:inventory')
    model = Asset
    ''' function to authorize user '''

    def get(self, *args, pk):
        if authorizeUser(self.request, pk):
            asset = Asset.objects.get(id=self.kwargs.get('pk'))
            asset_list = Asset.objects.filter(owner=self.request.user).order_by('name')
            return render(self.request, self.template_name, {'asset_delete': asset, 'asset_list': asset_list})
        return redirect('sale:dashboard')


class SearchAssetView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/search_asset.html'
    context_object_name = 'all_asset'

    def get_queryset(self):
        asset_name = self.request.GET.get('asset_name')
        if asset_name:
            return Asset.objects.filter(name__icontains=asset_name)
        return Asset.objects.all().order_by('-created_at', 'name')


class SearchUser(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/search_user.html'
    context_object_name = 'all_users'

    def get_queryset(self):
        username = self.request.GET.get('username')
        if username:
            return User.objects.filter(username__icontains=username)
        return User.objects.all().order_by('username').exclude(username='admin')


def getInterest(request):
    if request.method == 'POST' and request.is_ajax():
        status = 'interest'
        data = json.loads(request.body)  # retrieve json data
        asset = Asset.objects.get(id=data)
        user = User.objects.get(username=request.user)
        if user in asset.interested_user.all():
            Notification.objects.filter(asset_id=data, interested_user=user).delete()
            asset.interested_user.remove(user)
            asset.save()
            status = 'not_interest'
        else:
            Notification(asset_id=asset, asset_owner=asset.owner, asset_name=asset.name, interested_user=user).save()
            asset.interested_user.add(user)
            asset.save()
            status = 'interest'
        return JsonResponse({'asset': asset.name, 'interest': status})
    return redirect('sale:search_asset')


class NotificationView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/notification.html'
    context_object_name = 'all_noty'

    def post(self, *args):
        noty_id = self.request.POST.getlist('checkbox')  # get checked box to delete noty
        if noty_id:
            for noty_id in noty_id:
                Notification.objects.get(id=noty_id).delete()
        else:
            Notification.objects.filter(asset_owner=self.request.user).delete()
        return redirect('sale:notification')

    def get_queryset(self):
        asset_name = self.request.GET.get('asset_name')
        if asset_name:
            return Notification.objects.filter(asset_owner=self.request.user,
                                               asset_name__icontains=asset_name).order_by('-date')
        return Notification.objects.filter(asset_owner=self.request.user).order_by('-date')


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'sale/settings.html'


class ProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = 'sale/profile.html'
    model = Profile
    context_object_name = 'profile'

    def post(self, *args, pk):
        user_id = User.objects.get(id=self.request.POST.get('user_id'))
        image = self.request.FILES.get('image')
        user = Profile.objects.get(user_id=user_id)
        if image:
            user.image = image
        user.address = self.request.POST.get('address')
        user.phone_number = self.request.POST.get('phone_number')
        user.bio = self.request.POST.get('bio')
        user.save()
        return redirect(reverse('sale:profile', kwargs={'pk': pk}))

    def get_object(self):
        return get_object_or_404(Profile, user_id=self.kwargs.get('pk'))


def authorizeUser(request, pk):
    try:
        asset_id = Asset.objects.get(id=pk)
    except Asset.DoesNotExist:
        return False
    if str(request.user) == str(asset_id.owner):
        return True
    return False
