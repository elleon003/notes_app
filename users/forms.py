from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from turnstile.fields import TurnstileField

class CustomUserCreationForm(UserCreationForm):
    turnstile = TurnstileField(theme='dark',)

    class Meta:
        model = CustomUser
        fields = ('email', )

class CustomAuthenticationForm(AuthenticationForm):
    turnstile = TurnstileField()

    def clean(self):
        cleaned_data = super().clean()
        if self.user_cache:
            email = self.user_cache.email
        return cleaned_data        


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
