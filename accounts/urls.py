from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import CustomLoginView
from django.urls import path
from .views import CustomLoginView, dashboard_redirect_view, register, activate_account
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("register/", register, name="register"),
    path("activate/<uidb64>/<token>/", activate_account, name="activate"),
    path("redirect/", dashboard_redirect_view, name="dashboard_redirect"),
]


app_name = "accounts"

urlpatterns = [
    # Redirect root /accounts/ to /accounts/register/
    path('', RedirectView.as_view(url='register/', permanent=False)),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("redirect/", dashboard_redirect_view, name="dashboard_redirect"),

    # Template-based views
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path('profile/', views.profile, name='profile'),
    path('dashboard-redirect/', views.dashboard_redirect_view, name='dashboard_redirect'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Password reset confirm
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    # DRF / JWT API routes
    path('api/register/', views.UserRegisterAPIView.as_view(), name='api_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', views.UserDetailAPIView.as_view(), name='api_profile'),
]
