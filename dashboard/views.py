# dashboard/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def employer_dashboard(request):
    return render(request, 'dashboard/employer_dashboard.html')

@login_required
def seeker_dashboard(request):
    return render(request, 'dashboard/seeker_dashboard.html')
