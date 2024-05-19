from django.urls import path

#Vistas
from .views import LoginFormView, LogoutFormView, CustomPasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='login/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'), name='password_reset_complete'),
]
