from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # اضافه شده برای Messaging
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse("accounts:dashboard_redirect")


User = get_user_model()

# -------------------------
# Template-based views
# -------------------------

@login_required
def dashboard_redirect_view(request):
    """
    هدایت کاربر به داشبورد مناسب بر اساس نقش
    """
    if request.user.role == "employer":
        return redirect("dashboard:employer_dashboard")
    elif request.user.role == "seeker":
        return redirect("dashboard:seeker_dashboard")
    elif request.user.role == "admin":
        return redirect("dashboard:admin_dashboard")
    messages.error(request, "نقش شما تعریف نشده است.")
    return redirect("accounts:login")


@login_required
def edit_profile(request):
    """
    صفحه ویرایش پروفایل (موقت - بعداً فرم و API کامل اضافه میشه)
    """
    messages.info(request, "در حال حاضر ویرایش پروفایل فعال نیست.")
    return render(request, "accounts/edit_profile.html")


@login_required
def profile(request):
    """
    نمایش پروفایل کاربر
    """
    return render(request, "accounts/profile.html")


def activate_account(request, uidb64, token):
    """
    فعال‌سازی حساب کاربر با ایمیل
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "حساب شما با موفقیت فعال شد! حالا می‌توانید وارد شوید.")
        return redirect("accounts:login")
    else:
        messages.error(request, "لینک فعال‌سازی نامعتبر است.")
        return redirect("accounts:register")


def register(request):
    """
    ثبت‌نام کاربر جدید (Template view) با پیام‌ها
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # فعال‌سازی بعد از ایمیل
            user.save()

            # ارسال ایمیل فعال‌سازی
            current_site = get_current_site(request)
            subject = "Activate your Smart Job Portal account"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse(
                "accounts:activate", kwargs={"uidb64": uid, "token": token}
            )
            activation_url = f"http://{current_site.domain}{activation_link}"

            message = render_to_string(
                "accounts/activation_email.html",
                {"user": user, "activation_url": activation_url},
            )

            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(
                request, "ثبت‌نام با موفقیت انجام شد! ایمیل فعال‌سازی ارسال شد."
            )
            return redirect("accounts:login")
        else:
            messages.error(request, "خطا در ثبت‌نام! لطفا فرم را بررسی کنید.")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# -------------------------
# DRF / JWT API views
# -------------------------

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserSerializer, UserRegisterSerializer

class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)

        request = self.request
        current_site = get_current_site(request)
        subject = "Activate your Smart Job Portal account"
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = reverse(
            "accounts:activate", kwargs={"uidb64": uid, "token": token}
        )
        activation_url = f"http://{current_site.domain}{activation_link}"

        message = render_to_string(
            "accounts/activation_email.html",
            {"user": user, "activation_url": activation_url},
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


class UserLoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]


class TokenRefreshAPIView(TokenRefreshView):
    permission_classes = [AllowAny]


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
