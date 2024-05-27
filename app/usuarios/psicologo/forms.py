from django import forms
from app.usuarios.psicologo.models import Psicologo

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
            'apellido': 'Ingrese sus Apellidos',
            'cedula': 'Ingrese su Cédula',
            'email': 'Ingrese su correo',
            'foto': 'Subir una foto',
            'celular': 'Ingrese su celular',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Cédula'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese su Email'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su numero celular '}),            
        }