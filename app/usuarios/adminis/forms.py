from django import forms
from django.contrib.auth.models import User
from app.usuarios.adminis.models import Adminis
from django.core.exceptions import ValidationError


class AdminisForm(forms.ModelForm):
    username = forms.CharField(label = "Ingrese su Username",widget= forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'username',
            'placeholder':'Ingrese su Username',
            'required':'required',
        }
    ))

    password =  forms.CharField(label = "Ingrese su contraseña",widget= forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':'password',
            'placeholder':'Ingrese su contraseña',
            'required':'required',
            'autocomplete':'new-password'
        }
    ))


    class Meta:
        model = Adminis
        fields = ['nombre', 'apellido','email','foto','celular','direccion','username', 'password']

        labels={
            'nombre':'Ingrese sus nombres',
            'apellido':'Ingrese sus apellidos',
            'email':'Ingrese su email',
            'foto':'Subir una Foto',
            'celular':'Ingrese su celular',
            'direccion':'Ingrese su dirección'
        }

        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese sus Nombres'}),
            'apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese sus Apellidos'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese su Email'}),
            'celular': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su número celular',
                    'pattern': '09[0-9]{8}',  # Expresión regular que acepta '09' seguido de 8 dígitos
                    'title': 'El número de celular debe comenzar con 09 y tener 10 dígitos'
                }
            ),
            'direccion':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su dirección'}),
        }

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')

        # Verifica que el número de celular tenga exactamente 10 dígitos y comience con '09'.
        if not celular.startswith('09'):
            raise ValidationError('El número de celular debe comenzar con 09.')
        if not celular.isdigit() or len(celular) != 10:
            raise ValidationError('El número de celular debe tener 10 dígitos numéricos.')

        return celular
