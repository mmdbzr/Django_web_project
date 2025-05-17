from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_employer', 'is_seeker']

    def clean(self):
        cleaned_data = super().clean()
        is_employer = cleaned_data.get('is_employer')
        is_seeker = cleaned_data.get('is_seeker')
        if is_employer and is_seeker:
            raise forms.ValidationError("Only one role can be selected.")
        if not is_employer and not is_seeker:
            raise forms.ValidationError("You must select a role.")
        return cleaned_data
