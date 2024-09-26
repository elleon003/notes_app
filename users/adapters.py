from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model
from django.db.models import Q

CustomUser = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return

        try:
            # Check if a user with this email already exists
            existing_user = CustomUser.objects.get(
                Q(email__iexact=user_email(user)) | Q(email__iexact=sociallogin.email_addresses[0].email)
            )
            
            # If we get here, we found a matching user
            sociallogin.connect(request, existing_user)
        except CustomUser.DoesNotExist:
            # No existing user, continue with the normal flow
            pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Ensure the user is active
        user.is_active = True
        user.save()
        
        return user

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.email = data.get('email')
        return user