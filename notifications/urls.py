from django.urls import path
from .views import notifications_list

app_name = 'notifications'

urlpatterns = [
    path('', notifications_list, name='list'),
]
