# terapias/forms.py
from django import forms
<<<<<<< HEAD
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


=======
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
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c
        
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['estudiante', 'asistio']