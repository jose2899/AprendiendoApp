from django.shortcuts import render, redirect
from django.contrib.auth import logout

#Vistas
from django.contrib.auth.views import  LoginView
from django.views.generic import RedirectView

#Imports
from proyectAprendiendo.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL

# Create your views here.

class LoginFormView(LoginView):
    template_name = 'login/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesion'
        return context

class LogoutFormView(RedirectView):
    pattern_name = LOGOUT_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)