#formulario
from django import forms
from app.calendario.models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['estudiante', 'titulo', 'fecha_termino', 'observacion']

        labels = {
            'estudiante': 'Estudiante',
            'titulo': 'Ingrese un Titulo',
            'fecha_termino': 'Ingrese la Fecha de Termino',
            'observacion': 'Ingrese una Observación',
        }

        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_termino': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control'}),
        }

        input_formats = {
            'fecha_termino': ['%Y-%m-%d'],  # Año-Mes-Día
        }
