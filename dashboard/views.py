from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from jobs.models import Job, Application
from notifications.models import Notification
from django.shortcuts import redirect

def dashboard_redirect_view(request):
    if request.user.is_superuser:
        return redirect('dashboard:admin_dashboard')
    elif request.user.is_employer:
        return redirect('dashboard:employer_dashboard')
    else:
        return redirect('dashboard:seeker_dashboard')


User = get_user_model()


@login_required
def employer_dashboard(request):
    if not request.user.is_employer:
        return render(request, 'dashboard/unauthorized.html')

    jobs = Job.objects.active().filter(user=request.user)
    applications = Application.objects.filter(job__in=jobs).select_related('user', 'job')
    notifications = request.user.notifications.order_by('-created_at')[:5]

    return render(request, 'dashboard/employer_dashboard.html', {
        'jobs': jobs,
        'applications': applications,
        'notifications': notifications,
    })


@login_required
def seeker_dashboard(request):
    if not request.user.is_seeker:
        return render(request, 'dashboard/unauthorized.html')

    applications = Application.objects.select_related('job').filter(user=request.user)
    notifications = request.user.notifications.order_by('-created_at')[:5]

    return render(request, 'dashboard/jobseeker_dashboard.html', {
        'applications': applications,
        'notifications': notifications,
    })


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return render(request, 'dashboard/unauthorized.html')

    users = User.objects.all()
    jobs = Job.objects.all()
    notifications = Notification.objects.order_by('-created_at')[:10]

    return render(request, 'dashboard/admin_dashboard.html', {
        'users': users,
        'jobs': jobs,
        'notifications': notifications,
    })
