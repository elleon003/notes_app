from django.contrib.auth import login as auth_login
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from .forms import CustomAuthenticationForm


class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('home')