from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from allauth.account.forms import SignupForm
from .models import CustomUser
import requests

INPUT_CLASSES = "w-full px-3 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-950 dark:focus:ring-purple-400 focus:border-transparent text-slate-900 dark:text-white"
READONLY_CLASSES = "w-full px-3 py-2 bg-slate-100 dark:bg-slate-600 border border-slate-300 dark:border-slate-500 rounded-md text-slate-700 dark:text-slate-300"

class TurnstileMixin:
    def clean(self):
        cleaned_data = super().clean()
        turnstile_response = self.data.get('cf-turnstile-response')
        
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

class CustomSignupForm(TurnstileMixin, SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.update({
                    'class': INPUT_CLASSES
                })

class CustomUserCreationForm(TurnstileMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.update({
                    'class': INPUT_CLASSES
                })

class CustomAuthenticationForm(TurnstileMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.update({
                    'class': INPUT_CLASSES
                })

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].widget.attrs.update({
            'class': READONLY_CLASSES,
            'readonly': True
        })
        self.fields['first_name'].widget.attrs.update({
            'class': INPUT_CLASSES
        })
        self.fields['last_name'].widget.attrs.update({
            'class': INPUT_CLASSES
        })

class EmailChangeForm(forms.Form):
    current_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': READONLY_CLASSES,
        'readonly': 'readonly'
    }))
    new_email = forms.EmailField(
        label="New Email Address",
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES
        })
    )
    confirm_new_email = forms.EmailField(
        label="Confirm New Email Address",
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASSES
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['current_email'].initial = user.email
        
    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get('new_email')
        confirm_email = cleaned_data.get('confirm_new_email')
        
        if new_email and confirm_email:
            if new_email != confirm_email:
                raise forms.ValidationError("New email addresses must match.")
            if CustomUser.objects.filter(email=new_email).exclude(pk=self.user.pk).exists():
                raise forms.ValidationError("This email address is already in use.")
        
        return cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_CLASSES
            })
