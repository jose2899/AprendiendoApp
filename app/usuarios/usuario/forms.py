from django import forms
from app.usuarios.usuario.models import Representante, Estudiante

class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = ['nombre', 'apellido','telefono','celular','email','cedula','servicios', 'otra_terapia','conocido','observacion']
        
        labels={
            'nombre':'Ingrese sus nombres',
            'apellido':'Ingrese sus apellidos',
            'telefono':'Ingrese su telefono',
            'celular':'Ingrese su celular',
            'email':'Ingrese su email',
            'cedula':'Ingrese su cedula',
            'servicios': 'Servicios',
            'otra_terapia':'Ingrese otra terapia',
            'conocido':'¿como conocio la institucion?',
            'Observacion':'Ingrese alguna observación'
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Teléfono'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Celular'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Email'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Cédula'}),
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

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre','apellido','genero','cedula','fecha_nacimiento',
                  'año_educacion','institucion_educativa','fecha','motivo', 'representante']
        
        labels = {
            'nombre': 'Ingrese sus nombres',
            'apellido': 'Ingrese sus Apellidos',
            'genero':'Ingrese su género',
            'cedula': 'Ingrese su Cédula',
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
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Cédula'}),
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