from django import forms
from django.contrib.auth.forms import SetPasswordForm

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')