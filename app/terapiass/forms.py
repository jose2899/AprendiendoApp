# terapias/forms.py
from django import forms
from django.forms import inlineformset_factory
from app.terapiass.models import Terapia, Horario, AsignacionFechaTerapia, Asistencia
from app.terapiass.models import DiaSemana
from app.usuarios.psicologo.models import Psicologo
from app.usuarios.usuario.models import Estudiante


class TerapiaForm(forms.ModelForm):
    class Meta:
        model = Terapia
        fields = ['paquete', 'psicologo', 'estudiante']
  
class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['dia_semana', 'hora_inicio']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
        }

HorarioFormSet = inlineformset_factory(Terapia, Horario, form=HorarioForm, extra=6, can_delete=True)

class FechaTerapiaForm(forms.ModelForm):
    class Meta:
        model = AsignacionFechaTerapia
        fields = ['fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }
        
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['estudiante', 'asistio']