from . import views, auth_views
from django.urls import path

app_name = 'sale'
urlpatterns = [
    path('registration/', auth_views.Registration.as_view(), name='registration'),
    path('login/', auth_views.logInUser, name='login'),
    path('change-password/', auth_views.changePassword, name='password'),
    path('change-username/', auth_views.changeUsername, name='username'),
    path('change-email/', auth_views.changeEmail, name='email'),

    path('', views.DashboardView.as_view(), name='dashboard'),
    path('add-asset/', views.CreateAssetView.as_view(), name='create_asset'),
    path('inventory/', views.InventoryView.as_view(), name='inventory'),
    path('asset-details/<pk>/', views.AssetDetailView.as_view(), name='asset_details'),
    path('delete-asset/<pk>/', views.DeleteAssetView.as_view(), name='delete_asset'),
    path('update-asset/<pk>/', views.UpdateAssetView.as_view(), name='update_asset'),
    path('search-asset/', views.SearchAssetView.as_view(), name='search_asset'),
    path('search-user/', views.SearchUser.as_view(), name='search_user'),
    path('asset-owner/<pk>/', views.AssetOwnerView.as_view(), name='asset_owner'),
    path('notification/', views.NotificationView.as_view(), name='notification'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('interest/', views.getInterest, name='interest'),
    path('profile/<pk>/', views.ProfileView.as_view(), name='profile'),
]
