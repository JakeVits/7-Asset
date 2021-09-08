from . import views, auth_views
from django.urls import path

app_name = 'sale'
urlpatterns = [
    path('registration/', auth_views.Registration.as_view(), name='registration'),
    path('login/', auth_views.logInUser, name='login'),
    path('change-password', auth_views.changePassword, name='password'),
    path('change-username', auth_views.changeUsername, name='username'),
    path('change-email', auth_views.changeEmail, name='email'),

    path('', views.DashboardView.as_view(), name='dashboard'),
    path('add-asset/', views.NewAssetView.as_view(), name='new_asset'),
    path('delete-asset/<pk>/', views.DeleteAssetView.as_view(), name='delete_asset'),
    path('update-asset/<pk>/', views.UpdateAssetView.as_view(), name='update_asset'),
    path('my-inventory/', views.InventoryView.as_view(), name='inventory'),
    path('search-asset/', views.SearchAssetView.as_view(), name='search'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    # path('details/<pk>/', views.UserDetailsView.as_view(), name='details'),
]
