from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect_view(request):
    if request.user.is_employer:
        return redirect('dashboard:employer_dashboard')
    elif request.user.is_seeker:
        return redirect('dashboard:seeker_dashboard')
    else:
        return redirect('login')  # یا نمایش پیام خطا

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/activation_success.html')  
    else:
        return render(request, 'accounts/activation_invalid.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your Smart Job Portal account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_url = f"http://{current_site.domain}{activation_link}"
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'activation_url': activation_url,
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            return render(request, 'accounts/email_sent.html')  
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
