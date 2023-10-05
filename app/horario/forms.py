from django import forms
from app.usuarios.usuario.models import Estudiante
from app.usuarios.psicologo.models import Psicologo
from app.horario.models import Horario

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['estudiante', 'terapia', 'psicologo', 'hora_inicio','hora_fin', 'dia']
        labels = {
            'estudiante': 'Estudiante',
            'terapia': 'Terapia',
            'psicologo': 'Psicólogo',
            'hora_inicio': 'Hora de la Clase',
            'hora_fin': 'Hora fin clase',
            'dia': 'Dia de semana',
        }
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        dia = cleaned_data.get('dia')
        estudiante = cleaned_data.get('estudiante')

        # Verificar si ya existe un horario para el estudiante en esa hora y día
        if Horario.objects.filter(estudiante=estudiante, hora_inicio=hora_inicio, dia=dia).exists():
            raise forms.ValidationError('El estudiante ya tiene clase en esa hora y día.')

        return cleaned_data
