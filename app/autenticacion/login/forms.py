from django import forms
from django.contrib.auth.forms import SetPasswordForm

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = "Nueva Contraseña"
        self.fields['new_password2'].label = "Confirmar Nueva Contraseña"
        
        self.fields['new_password1'].help_text =(
            "Debe contener al menos 8 caracteres, no ser comúnmente utilizada y no puede ser completamente numérica."
        )
        self.fields['new_password2'].help_text =(
            "Introduce nuevamente la nueva contraseña para confirmar."
        )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        # Añadir validaciones adicionales aquí si es necesario
        if len(password1) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        if password1.isdigit():
            raise forms.ValidationError(
                "La contraseña no puede ser completamente numérica."
            )
        # Puedes añadir más validaciones personalizadas aquí
        return password1
    