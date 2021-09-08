from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy, reverse
from .models import User, Asset, Account
from .forms import AssetForm
from django.shortcuts import redirect, render


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'sale/dashboard.html'


class NewAssetView(LoginRequiredMixin, generic.CreateView):
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
        return render(self.request, 'sale/new_asset.html', {'form': self.form_class})

    def form_invalid(self, form):
        print('==========================', 'File is not valid', '================================')
        print('==========================', self.request.FILES.get('image'), '================================')
        messages.warning(self.request, 'Failed to add stock!')
        return redirect('sale:new_asset')


class DeleteAssetView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'sale/inventory.html'
    success_url = reverse_lazy('sale:inventory')
    model = Asset

    def get(self, *args, pk):
        if authorizeUser(self.request, pk):
            asset = Asset.objects.get(id=self.kwargs.get('pk'))
            asset_list = Asset.objects.filter(owner=Account(username=self.request.user))
            return render(self.request, self.template_name, {'delete_asset': asset, 'asset_list': asset_list})
        messages.warning(self.request, 'You are not authorized!')
        return redirect('sale:dashboard')


class UpdateAssetView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'sale/update_asset.html'
    form_class = AssetForm
    model = Asset
    context_object_name = 'update_asset'
    success_url = reverse_lazy('sale:inventory')

    def get(self, *args, pk):
        if authorizeUser(self.request, pk):
            return render(self.request, self.template_name, {'update_asset': Asset.objects.get(id=self.kwargs.get('pk'))})
        messages.warning(self.request, 'You are not authorized!')
        return redirect('sale:dashboard')

    def form_valid(self, form):
        asset = form.save(commit=False)
        asset.name = form.cleaned_data['name'].title().strip()
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Failed to update stock!')
        return redirect('sale:update_asset', pk=self.kwargs.get('pk'))


class InventoryView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/inventory.html'

    def get_queryset(self):
        return Asset.objects.filter(owner=Account(username=self.request.user)).order_by('name')

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
        else:
            return Asset.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['all_asset'] = self.get_queryset()
        return context


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'sale/settings.html'


def authorizeUser(request, pk):
    asset_id = Asset.objects.get(id=pk)
    if str(request.user) == str(asset_id.owner):
        return True
    return False


# def searchAsset(request):
#     template_name = 'sale/search_asset.html'
#     if request.method == 'GET':
#         asset_name = request.GET.get('asset_name')
#         if asset_name:
#             asset_list = Asset.objects.filter(name__icontains=asset_name)
#             return render(request, template_name, {'asset_list': asset_list})
#         return render(request, template_name)
