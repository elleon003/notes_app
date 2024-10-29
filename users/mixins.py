import requests
from django import forms
from django.conf import settings

class TurnstileMixin:
    def clean(self):
        cleaned_data = super().clean()
        turnstile_response = cleaned_data.get('cf-turnstile-response')
        
        if not turnstile_response:
            raise forms.ValidationError(
                'Please complete the Turnstile challenge.',
                code='invalid_turnstile'
            )

        # Verify the token with Cloudflare
        data = {
            'secret': settings.TURNSTILE_SECRET,
            'response': turnstile_response,
        }
        
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data=data
        )
        
        if not response.ok or not response.json().get('success'):
            raise forms.ValidationError(
                'Turnstile validation failed. Please try again.',
                code='invalid_turnstile'
            )
            
        return cleaned_data
