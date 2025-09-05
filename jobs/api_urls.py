from django.urls import path
from .api_views import (
    JobListAPIView,
    JobDetailAPIView,
    JobCreateAPIView,
    ApplicationCreateAPIView,
    ApplicationListAPIView
)

app_name = 'jobs-api'

urlpatterns = [
    # -------------------------
    # Jobs
    # -------------------------
    path('jobs/', JobListAPIView.as_view(), name='job-list'),
    path('jobs/create/', JobCreateAPIView.as_view(), name='job-create'),
    path('jobs/<int:pk>/', JobDetailAPIView.as_view(), name='job-detail'),

    # -------------------------
    # Applications
    # -------------------------
    path('applications/', ApplicationListAPIView.as_view(), name='application-list'),
    path('applications/create/', ApplicationCreateAPIView.as_view(), name='application-create'),
]
