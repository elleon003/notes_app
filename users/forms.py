from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
import requests

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', )

class CustomAuthenticationForm(AuthenticationForm):
    cf_turnstile_response = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        cf_turnstile_response = cleaned_data.get('cf_turnstile_response')

        if not cf_turnstile_response:
            raise forms.ValidationError('Turnstile validation failed. Please try again.')

        # Verify Turnstile response
        data = {
            'secret': settings.TURNSTILE_SECRET,
            'response': cf_turnstile_response,
        }
        response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
        result = response.json()

        if not result.get('success'):
            raise forms.ValidationError('Turnstile validation failed. Please try again.')

        if self.user_cache:
            email = self.user_cache.email
        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
