from django.contrib.auth import views as auth_views
from django.conf import settings
from .forms import CustomAuthenticationForm

class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turnstile_sitekey'] = settings.TURNSTILE_SITEKEY
        return context