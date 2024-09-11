from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test-google-template/', views.test_google_login_template, name='test_google_template'),
]
