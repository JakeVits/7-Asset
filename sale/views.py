from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy, reverse
from .models import User, Asset, Profile, Notification
from .forms import AssetForm
from django.shortcuts import redirect, render
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


class DeleteAssetView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'sale/inventory.html'
    success_url = reverse_lazy('sale:inventory')
    model = Asset

    def get(self, *args, pk):
        if authorizeUser(self.request, pk):
            asset = Asset.objects.get(id=self.kwargs.get('pk'))
            asset_list = Asset.objects.filter(owner=self.request.user).order_by('name')
            return render(self.request, self.template_name, {'asset_delete': asset, 'asset_list': asset_list})
        return redirect('sale:dashboard')


class UpdateAssetView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'sale/update_asset.html'
    form_class = AssetForm
    model = Asset
    context_object_name = 'update_asset'

    def get(self, *args, pk):
        if authorizeUser(self.request, pk):
            return render(self.request, self.template_name, {'update_asset': Asset.objects.get(id=self.kwargs.get('pk'))})
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


class InventoryView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/inventory.html'

    def get_queryset(self):
        return Asset.objects.filter(owner=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['asset_list'] = self.get_queryset()
        return context


class SearchAssetView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/search_asset.html'

    def get_queryset(self):
        asset_name = self.request.GET.get('asset_name')
        if asset_name:
            return Asset.objects.filter(name__icontains=asset_name)
        return Asset.objects.all().order_by('-created_at', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['all_asset'] = self.get_queryset()
        # context['current_user'] = User.objects.get(username=self.request.user)
        return context


def getInterest(request):
    if request.method == 'POST' and request.is_ajax():
        status = 'interest'
        data = json.loads(request.body)  # retrieve json data
        asset = Asset.objects.get(id=data)
        user = User.objects.get(username=request.user)
        if user in asset.interested_user.all():
            Notification.objects.filter(asset_id=data, interested_user=user).delete()
            asset.total_interest -= 1
            asset.interested_user.remove(user)
            asset.save()
            status = 'not_interest'
        else:
            Notification(asset_id=asset, asset_owner=asset.owner, asset_name=asset.name, interested_user=user).save()
            asset.total_interest += 1
            asset.interested_user.add(user)
            asset.save()
            status = 'interest'
        return JsonResponse({'asset': asset.name, 'interest': status})
    return redirect('sale')


class NotificationView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/notification.html'

    def get_queryset(self):
        return Notification.objects.filter(asset_owner=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['all_noty'] = self.get_queryset()
        return context


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'sale/settings.html'


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'sale/profile.html'


def authorizeUser(request, pk):
    try:
        asset_id = Asset.objects.get(id=pk)
    except Asset.DoesNotExist:
        return False
    if str(request.user) == str(asset_id.owner):
        return True
    return False

# class InterestView(LoginRequiredMixin, generic.CreateView):
#     template_name = 'sale/search_asset.html'
#     fields = ['']
#     success_url = reverse_lazy('sale:search')
#
#     def post(self, *args):
#         status = self.request.get.POST()


# def searchAsset(request):
#     template_name = 'sale/search_asset.html'
#     if request.method == 'GET':
#         asset_name = request.GET.get('asset_name')
#         if asset_name:
#             asset_list = Asset.objects.filter(name__icontains=asset_name)
#             return render(request, template_name, {'asset_list': asset_list})
#         return render(request, template_name)
