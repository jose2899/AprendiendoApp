# terapias/forms.py
from django import forms
from app.terapiass.models import Terapia, AsignacionEstudiante, AsignacionPsicologo, HorarioTerapia
from app.terapiass.models import DiaSemana
from app.terapiass.utils import calculate_start_date
from datetime import datetime, timedelta
from app.usuarios.usuario.models import Estudiante
from app.usuarios.psicologo.models import Psicologo
from django.forms.widgets import CheckboxSelectMultiple
from app.servicios.models import Paquete
from django.forms import formset_factory
from django.forms import modelformset_factory


class TerapiaForm(forms.ModelForm):
    class Meta:
        model = Terapia
        fields = ['paquete', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AsignacionPsicologoForm(forms.ModelForm):
    
    dia_semana = forms.ModelMultipleChoiceField(
        queryset=DiaSemana.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = AsignacionPsicologo
        fields = ['psicologo', 'dia_semana']

    def __init__(self, *args, **kwargs):
        super(AsignacionPsicologoForm, self).__init__(*args, **kwargs)
        self.fields['dia_semana'].widget.attrs.update({'class': 'selectpicker'})
    
    def set_dia_semana_choices(self):
        self.fields['dia_semana'].choices = [(dia.nombre, dia.nombre) for dia in DiaSemana.objects.all()]

AsignacionPsicologoFormSet = modelformset_factory(AsignacionPsicologo, form=AsignacionPsicologoForm, extra=1)


class AsignacionEstudianteForm(forms.ModelForm):
    class Meta:
        model = AsignacionEstudiante
        fields = ['estudiante']


class HorarioTerapiaForm(forms.ModelForm):
    class Meta:
        model = HorarioTerapia
        fields = ['asignacion_psicologo', 'hora_inicio', 'hora_fin']

HorarioTerapiaFormSet = forms.inlineformset_factory(AsignacionPsicologo, HorarioTerapia, form=HorarioTerapiaForm, extra=0)
