from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from turnstile.fields import TurnstileField

class CustomUserCreationForm(UserCreationForm):
    turnstile = TurnstileField(theme='dark',)

    class Meta:
        model = CustomUser
        fields = ('email', )

class CustomAuthenticationForm(AuthenticationForm):
    turnstile = TurnstileField(theme='dark',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turnstile'].widget.attrs['data-sitekey'] = settings.TURNSTILE_SITE_KEY

    def clean(self):
        cleaned_data = super().clean()
        if self.user_cache:
            email = self.user_cache.email
        return cleaned_data        


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
