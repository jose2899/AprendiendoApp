from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse_lazy
from app.autenticacion.login.forms import PasswordResetForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from django.utils.http import urlsafe_base64_decode
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
    
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'login/password_reset.html'
    email_template_name = 'login/password_reset_email.html'
    success_url = reverse_lazy('password_reset')  
    success_message = "El correo electrónico para restablecer la contraseña ha sido enviado."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
