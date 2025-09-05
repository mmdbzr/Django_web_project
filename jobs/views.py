from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, path, include
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.routers import DefaultRouter
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer, ApplicationCreateSerializer
from .permissions import IsEmployer, IsSeeker, IsOwnerOrReadOnly, IsAdmin

# -------------------------
# Job Views (HTML)
# -------------------------

class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        jobs = Job.objects.active()
        if query:
            jobs = jobs.filter(title__icontains=query)
        return jobs


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['title', 'description', 'location', 'salary', 'is_active']
    template_name = 'job_form.html'

    def form_valid(self, form):
        if self.request.user.is_employer:
            form.instance.user = self.request.user
            response = super().form_valid(form)

            # ✉️ ارسال ایمیل اطلاع‌رسانی
            subject = 'شغل جدید شما با موفقیت ثبت شد'
            message = f"""
سلام {self.request.user.username} عزیز،
شغل جدید شما با عنوان "{form.instance.title}" ثبت شد.
با احترام، تیم اسمارت‌جاب
"""
            send_mail(subject, message, settings.EMAIL_HOST_USER, [self.request.user.email])
            messages.success(self.request, "شغل جدید ثبت و ایمیل اطلاع‌رسانی ارسال شد.")
            return response
        else:
            messages.error(self.request, "فقط کارفرما می‌تواند شغل ایجاد کند!")
            return redirect('jobs:job-list')

    def get_success_url(self):
        return reverse_lazy('dashboard:employer_dashboard')


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    fields = ['title', 'description', 'location', 'salary', 'is_active']
    template_name = 'job_form.html'

    def form_valid(self, form):
        messages.success(self.request, "اطلاعات شغل با موفقیت بروزرسانی شد.")
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.user

    def get_success_url(self):
        return reverse_lazy('dashboard:employer_dashboard')


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = "job_confirm_delete.html"

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "شغل با موفقیت حذف شد.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('dashboard:employer_dashboard')


# -------------------------
# API Views (DRF)
# -------------------------

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsEmployer() | IsAdmin(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsSeeker()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticated()]


# -------------------------
# URLs
# -------------------------

app_name = 'jobs'

# HTML urls
urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
]

# API urls (router)
router = DefaultRouter()
router.register(r'api/jobs', JobViewSet)
router.register(r'api/applications', ApplicationViewSet)

urlpatterns += [
    path('', include(router.urls)),
]
