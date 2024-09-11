from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from allauth.socialaccount.models import SocialAccount

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        if self.user_cache:
            email = self.user_cache.email 
            try:
                social_account = SocialAccount.objects.get(user__email=email, provider='google')
                self.confirm_login_allowed(self.user_cache)
            except SocialAccount.DoesNotExist:
                pass
        return cleaned_data