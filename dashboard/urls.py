
from django.urls import path
from .views import employer_dashboard, seeker_dashboard, admin_dashboard, dashboard_redirect_view
from .views import employer_dashboard, seeker_dashboard, admin_dashboard, dashboard_redirect_view

app_name = 'dashboard'


urlpatterns = [
       path('employer/', employer_dashboard, name='employer_dashboard'),
       path('seeker/', seeker_dashboard, name='seeker_dashboard'),
       path('admin/', admin_dashboard, name='admin_dashboard'),
       path('redirect/', dashboard_redirect_view, name='dashboard_redirect'),
   ]
