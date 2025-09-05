from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib import admin  # اضافه کردن این خط

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('api.urls')),
    path('', RedirectView.as_view(url='/jobs/', permanent=False)),
    path('notifications/', include('notifications.urls')),

]