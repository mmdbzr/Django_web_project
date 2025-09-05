from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("ایمیل"),
        help_text=_("لطفاً یک آدرس ایمیل معتبر وارد کنید.")
    )
    is_employer = forms.BooleanField(
        required=False,
        label=_("کارفرما"),
        help_text=_("انتخاب کنید اگر کارفرما هستید.")
    )
    is_seeker = forms.BooleanField(
        required=False,
        label=_("کارجو"),
        help_text=_("انتخاب کنید اگر کارجو هستید.")
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_employer', 'is_seeker']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("این ایمیل قبلاً ثبت شده است."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        is_employer = cleaned_data.get('is_employer')
        is_seeker = cleaned_data.get('is_seeker')

        if is_employer and is_seeker:
            raise forms.ValidationError(_("فقط یکی از نقش‌ها می‌تواند انتخاب شود."))
        if not is_employer and not is_seeker:
            raise forms.ValidationError(_("لطفاً یکی از نقش‌ها را انتخاب کنید."))
        return cleaned_data