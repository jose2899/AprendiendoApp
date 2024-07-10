from django.http import HttpResponse
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
from .forms import CustomSetPasswordForm
from django.views import View

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
    
    
class RecuperarContrasenaView(PasswordResetView):
    template_name = 'login/recuperarContrasena.html'
    email_template_name = 'login/recuperarContrasenaEmail.html'
    success_url = reverse_lazy('recuperar_contrasena')  
    success_message = "El correo electrónico para restablecer la contraseña ha sido enviado."

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(self.request,("El correo electrónico proporcionado no existe."))
            return redirect('recuperar_contrasena')
        else:
            messages.success(self.request,("El correo se envio con exito."))
            return super().form_valid(form)
    
class ConfirmarRecuperacionContrasenaView(PasswordResetConfirmView):
    template_name = 'login/confirmarRecuperacionContrasena.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('recuperar_contrasena_completa')

    def form_valid(self, form):
        messages.success(self.request, "La contraseña ha sido restablecida exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors.as_data()
        if 'new_password1' in errors:
            messages.error(self.request, "La contraseña debe cumplir con los requisitos establecidos.")
        else:
            for field, error_messages in errors.items():
                for error in error_messages:
                    messages.error(self.request, error.message)
        return super().form_invalid(form)
    

class RecuperacionContrasenaCompletaView(View):
    template_name = 'login/recuperacionContrasenaCompleta.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)