from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer, ApplicationCreateSerializer

# -------------------------
# Job API Views
# -------------------------

class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.active()
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]  # همه میتونن ببینن

    def get_queryset(self):
        query = self.request.GET.get('q')
        jobs = super().get_queryset()
        if query:
            jobs = jobs.filter(title__icontains=query)
        return jobs


class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]


class JobCreateAPIView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_employer:
            raise permissions.PermissionDenied("فقط کارفرمایان می‌توانند شغل ایجاد کنند.")
        serializer.save(user=user)


# -------------------------
# Application API Views
# -------------------------

class ApplicationCreateAPIView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplicationListAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # اگر کارفرما: نمایش اپلای‌های شغل‌های خودش
        if user.is_employer:
            return Application.objects.filter(job__user=user)
        # اگر کارجو: نمایش اپلای‌های خودش
        return Application.objects.filter(user=user)
