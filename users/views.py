from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import UpdateView, FormView
from django.contrib import messages
from django.views.generic.base import TemplateView
from allauth.socialaccount.models import SocialAccount

from .forms import (
    CustomAuthenticationForm, 
    UserProfileForm, 
    EmailChangeForm, 
    CustomPasswordChangeForm
)
from .models import CustomUser


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


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_account'] = SocialAccount.objects.filter(
            user=self.request.user, 
            provider='google'
        ).first()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)


class EmailChangeView(LoginRequiredMixin, FormView):
    form_class = EmailChangeForm
    template_name = 'users/email_change.html'
    success_url = reverse_lazy('users:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['new_email']
        user.save()
        messages.success(self.request, 'Your email has been updated successfully.')
        return super().form_valid(form)


class CustomPasswordChangeView(LoginRequiredMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)


class GoogleAccountManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'users/google_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_account'] = SocialAccount.objects.filter(
            user=self.request.user, 
            provider='google'
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'unlink':
            SocialAccount.objects.filter(
                user=request.user, 
                provider='google'
            ).delete()
            messages.success(request, 'Google account has been unlinked successfully.')
        return redirect('users:profile')
