# terapias/forms.py
from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from app.terapiass.models import Asistencia, HorarioTerapia
from app.terapiass.models import DiaSemana
from app.usuarios.psicologo.models import Psicologo
from app.usuarios.usuario.models import Estudiante
from app.servicios.models import Paquete



class HorarioTerapiaForm(forms.ModelForm):
    class Meta:
        model = HorarioTerapia
        fields = ['paquete','psicologo','dia_semana', 'hora_inicio']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'paquete': forms.TextInput(attrs={'readonly':True}),
        }
    def __init__(self, *args, **kwargs):
        paquete_id = kwargs.pop('paquete_id', None)
        super(HorarioTerapiaForm, self).__init__(*args, **kwargs)
        if paquete_id:
            self.fields['paquete'].initial = paquete_id
            self.fields['paquete'].widget = forms.HiddenInput() 
HorarioTerapiaFormSet = modelformset_factory(HorarioTerapia, form=HorarioTerapiaForm, extra=4)

class FechaInicioForm(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha de Inicio',
        widget=forms.DateInput(attrs={'type': 'date'})
    )


        
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['estudiante', 'asistio']