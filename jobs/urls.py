from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
    JobViewSet,
    ApplicationViewSet,
)

app_name = 'jobs'

# -------------------------
# HTML URLS
# -------------------------
urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
]

# -------------------------
# API URLS - DRF Router
# -------------------------
router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job-api')
router.register(r'applications', ApplicationViewSet, basename='application-api')

urlpatterns += [
    path('api/', include(router.urls)),  # یعنی زیر /jobs/api/
]