from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView


class UsersLogin(LoginView):
    template_name = 'users/login.html'


def logout_view(request):
    logout(request)
    return redirect('login')
