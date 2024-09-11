from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect 
from django.contrib import messages 
from django.contrib.auth import get_user_model

User = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # this hook is called before the social login is attempted
        user = sociallogin.user
        if user.id:
            return
        try:
            # Check if email already exists
            existing_user = self.get_model('user').objects.get(email=user.email)
            # If it does, connect this social account to the existing user
            sociallogin.connect(request, existing_user)
            # Add a success message
            messages.success(request, "Successfully connected your account with Google.")
        except self.get_model('user').DoesNotExist:
            pass