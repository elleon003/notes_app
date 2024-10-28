from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
import requests

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomAuthenticationForm(AuthenticationForm):
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
            'class': 'w-full px-3 py-2 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-950 focus:border-transparent',
            'readonly': True
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-950 focus:border-transparent'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-950 focus:border-transparent'
        })

class EmailChangeForm(forms.Form):
    current_email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 bg-slate-100 border border-slate-300 rounded-md',
        'readonly': 'readonly'
    }))
    new_email = forms.EmailField(
        label="New Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-950 focus:border-transparent'
        })
    )
    confirm_new_email = forms.EmailField(
        label="Confirm New Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-950 focus:border-transparent'
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
                'class': 'w-full px-3 py-2 bg-white border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-950 focus:border-transparent'
            })
