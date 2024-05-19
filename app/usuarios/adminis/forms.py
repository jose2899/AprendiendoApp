from django import forms
from django.contrib.auth.models import User
from app.usuarios.adminis.models import Adminis

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
            'direccion':'Ingrese su direccion'
        }

        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese sus Nombres'}),
            'apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese sus Apellidos'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese su Email'}),
            'celular':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su celular'}),
            'direccion':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su direccion'}),
        }
