from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def notifications_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'notifications/notifications_list.html', {
        'notifications': notifications
    })
