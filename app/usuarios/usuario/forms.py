from django import forms
from app.usuarios.usuario.models import Representante, Estudiante
from django.core.exceptions import ValidationError


class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = ['nombre', 'apellido','telefono','celular','email','cedula','servicios', 'otra_terapia','conocido','observacion']
        
        labels={
            'nombre':'Ingrese sus nombres',
            'apellido':'Ingrese sus apellidos',
            'telefono':'Ingrese su teléfono',
            'celular':'Ingrese su celular',
            'email':'Ingrese su email',
            'cedula':'Ingrese su cédula',
            'servicios': 'Servicios',
            'otra_terapia':'Ingrese otra terapia',
            'conocido':'¿Como conocio la institución?',
            'observacion':'Ingrese alguna observación'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Teléfono (opcional)'}),
            'celular': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su número celular',
                    'pattern': '09[0-9]{8}',
                    'title': 'El número de celular debe comenzar con 09 y tener 10 dígitos'
                }
            ),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Email'}),
            'cedula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su Cédula',
                    'pattern': '[0-9]{10}',
                    'title': 'La cédula debe tener 10 dígitos numéricos'
                }
            ),
            'servicios': forms.Select(attrs={'class': 'form-control'}),
            'otra_terapia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Otra terapia (opcional)'}),
            'conocido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cómo nos conoció'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
        }

    def __init__(self, *args, **kwargs):
        super(RepresentanteForm, self).__init__(*args, **kwargs)
        self.fields['otra_terapia'].required = False
        self.fields['observacion'].required = False
        self.fields['telefono'].required = False
    
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

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre','apellido','genero','cedula','fecha_nacimiento',
                  'año_educacion','institucion_educativa','fecha','motivo', 'representante']
        
        labels = {
            'nombre': 'Ingrese sus nombres',
            'apellido': 'Ingrese sus apellidos',
            'genero':'Ingrese su género',
            'cedula': 'Ingrese su cédula',
            'fecha_nacimiento': 'Ingrese su Fecha de Nacimiento',
            'año_educacion': 'Ingrese su Año de Educación',
            'institucion_educativa': 'Ingrese su Institución Educativa',
            'fecha': 'Fecha',
            'motivo': 'Ingrese su Motivo',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su Cédula',
                    'pattern': '[0-9]{10}',
                    'title': 'La cédula debe tener 10 dígitos numéricos'
                }
            ),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'año_educacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Año de Educación '}),
            'institucion_educativa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institución Educativa'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Motivo'}),
            'representante':forms.Select(attrs={'class': 'form-control'}),
        }

        input_formats = {
            'fecha': ['%Y-%m-%d'],  # Año-Mes-Día
        }

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para el representante
        self.fields['representante'].queryset = Representante.objects.all()

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