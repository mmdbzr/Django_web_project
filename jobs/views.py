from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Job

class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        jobs = Job.objects.active()  # استفاده از Custom Manager برای فیلتر مشاغل فعال
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
        if self.request.user.is_employer:  # فقط کارفرمایان اجازه ایجاد شغل دارند
            form.instance.user = self.request.user
            messages.success(self.request, "شغل جدید با موفقیت اضافه شد!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "فقط کارفرمایان می‌توانند شغل ایجاد کنند!")
            return redirect('job_list')

class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ['title', 'description', 'location', 'salary', 'is_active']
    template_name = 'job_form.html'

    def form_valid(self, form):
        messages.success(self.request, "اطلاعات شغل با موفقیت بروزرسانی شد!")
        return super().form_valid(form)

class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(request, "شغل با موفقیت حذف شد!")
        return super().delete(request, *args, **kwargs)
