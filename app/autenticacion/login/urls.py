from django.urls import path

#Vistas
from .views import LoginFormView, LogoutFormView, RecuperarContrasenaView, ConfirmarRecuperacionContrasenaView, RecuperacionContrasenaCompletaView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('recuperarContrasena/', RecuperarContrasenaView.as_view(), name='recuperar_contrasena'),
    path('confirmarRecuperacionContrasena/<uidb64>/<token>/', ConfirmarRecuperacionContrasenaView.as_view(), name='confirmar_recuperacion_contrasena'),
    path('recuperacionContrasenaCompleta/', RecuperacionContrasenaCompletaView.as_view(), name='recuperar_contrasena_completa'),
]
