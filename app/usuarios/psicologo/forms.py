from django import forms
from app.usuarios.psicologo.models import Psicologo
from django.core.exceptions import ValidationError

class PsicologoForm(forms.ModelForm):
    username = forms.CharField(label="Ingrese su cuenta", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su cuenta',
            'required': 'required',
        }
    ))

    password = forms.CharField(label="Ingrese su contraseña", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'required': 'required',
            'autocomplete': 'new-password'
        }
    ))

    class Meta:
        model = Psicologo
        fields = ['nombre', 'apellido','cedula','email','foto','celular','username', 'password']
        
        labels = {
            'nombre': 'Ingrese sus nombres',
            'apellido': 'Ingrese sus apellidos',
            'cedula': 'Ingrese su cédula',
            'email': 'Ingrese su correo',
            'foto': 'Subir una foto',
            'celular': 'Ingrese su celular',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
            'cedula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su Cédula',
                    'pattern': '[0-9]{10}',
                    'title': 'La cédula debe tener 10 dígitos numéricos'
                }
            ),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese su Email'}),
            'celular': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su número celular',
                    'pattern': '09[0-9]{8}',  # Expresión regular que acepta '09' seguido de 8 dígitos
                    'title': 'El número de celular debe comenzar con 09 y tener 10 dígitos'
                }
            )            
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        
        # Verifica si la cédula tiene exactamente 10 dígitos y todos son números.
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValidationError('La cédula debe tener 10 dígitos numéricos.')

        # Verifica los dos primeros dígitos (provincia).
        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            raise ValidationError('Los dos primeros dígitos de la cédula no son válidos. Deben estar entre 01 y 24.')

        # Verifica que el tercer dígito sea menor que 6.
        tercer_digito = int(cedula[2])
        if tercer_digito >= 6:
            raise ValidationError('El tercer dígito de la cédula no es válido. Debe ser menor que 6.')
        return cedula
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular')

        # Verifica que el número de celular tenga exactamente 10 dígitos y comience con '09'.
        if not celular.startswith('09'):
            raise ValidationError('El número de celular debe comenzar con 09.')
        if not celular.isdigit() or len(celular) != 10:
            raise ValidationError('El número de celular debe tener 10 dígitos numéricos.')

        return celular