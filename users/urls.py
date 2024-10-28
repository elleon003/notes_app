from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/email/', views.EmailChangeView.as_view(), name='email_change'),
    path('profile/password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('profile/google/', views.GoogleAccountManagementView.as_view(), name='google_account'),
]
