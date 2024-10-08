from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return redirect('idea_list')


def test_google_login_template(request):
    return render(request, 'socialaccount/providers/google/login.html', {'process': 'login'})