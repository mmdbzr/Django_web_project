from django.contrib.auth import views as auth_views
from django.urls import path
from .views import register
from .views import activate_account
from . import views
from .views import dashboard_redirect_view

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),        path('profile/', views.profile, name='profile'),
    path('dashboard-redirect/', dashboard_redirect_view, name='dashboard_redirect'),


]

