# dashboard/urls.py

from django.urls import path
from .views import employer_dashboard, seeker_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('employer/', employer_dashboard, name='employer_dashboard'),
    path('seeker/', seeker_dashboard, name='seeker_dashboard'),
]
