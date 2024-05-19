from django import forms
from app.planificaciones.models import Planificacion, PlanificacionSemana
from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico

class PlanificacionForm(forms.ModelForm):
    class Meta:
        model = Planificacion
        fields = ['estudiante', 'diagnostico', 'edad_biologica', 'edad_cognitiva_lenguaje_verbal', 'edad_cognitiva_lenguaje_comprensivo']
        labels = {
            'edad_biologica': 'Edad Biológica',
            'edad_cognitiva_lenguaje_verbal': 'Edad Cognitiva - Lenguaje Verbal',
            'edad_cognitiva_lenguaje_comprensivo': 'Edad Cognitiva - Lenguaje Comprensivo',
        }
        widgets = {
            'estudiante':forms.Select(attrs={'class': 'form-control'}),
            'diagnostico':forms.Select(attrs={'class': 'form-control'}),
            'edad_biologica': forms.NumberInput(attrs={'class': 'form-control'}),
            'edad_cognitiva_lenguaje_verbal': forms.NumberInput(attrs={'class': 'form-control'}),
            'edad_cognitiva_lenguaje_comprensivo': forms.NumberInput(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super(PlanificacionForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para el estudiante
        self.fields['estudiante'].queryset = Estudiante.objects.all()
    
    def __init__(self, *args, **kwargs):
        super(PlanificacionForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para la planificacion
        self.fields['diagnostico'].queryset = Diagnostico.objects.all()
    

class PlanificacionSemanaForm(forms.ModelForm):
    class Meta:
        model = PlanificacionSemana
        fields = ['planificacion','numero_semana', 'tiempo_previsto', 'objetivo', 'actividad_lenguaje', 'actividad_cognitiva', 'actividad_sensorial', 'actividades_internalizadas', 'actividades_reforzar']
        labels = {
            'numero_semana': 'Numero Semana',
            'tiempo_previsto': 'Tiempo Previsto',
            'objetivo': 'Objetivo',
            'actividad_lenguaje': 'Actividad lenguaje',
            'actividad_cognitiva': 'Actividad Cognitiva',
            'actividad_sensorial': 'Actividad Sensorial',
            'actividades_internalizadas': 'Actividades Internalizadas',
            'actividades_reforzar': 'Actividades Reforzar'
        }
        widgets = {
            'planificacion':forms.Select(attrs={'class': 'form-control'}),
            'numero_semana': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiempo_previsto': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control'}),
            'actividad_lenguaje': forms.TextInput(attrs={'class': 'form-control'}),
            'actividad_cognitiva': forms.TextInput(attrs={'class': 'form-control'}),
            'actividad_sensorial': forms.TextInput(attrs={'class': 'form-control'}),
            'actividades_internalizadas' : forms.TextInput(attrs={'class': 'form-control'}),
            'actividades_reforzar' : forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PlanificacionSemanaForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para la planificacion
        self.fields['planificacion'].queryset = Planificacion.objects.all()

