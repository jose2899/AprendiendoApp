# terapias/forms.py
from django import forms
from app.terapias.models import Terapia, AsignacionEstudiante
from app.terapias.models import DIAS_SEMANA_CHOICES
from app.terapias.utils import calculate_start_date
from datetime import datetime, timedelta
from app.usuarios.usuario.models import Estudiante

class TerapiaForm(forms.ModelForm):
    dia_semana = forms.MultipleChoiceField(
        choices=DIAS_SEMANA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Terapia
        fields = ['psicologo', 'paquete', 'dia_semana', 'fecha_inicio']

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }   

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        dia_semana_seleccionados = self.cleaned_data['dia_semana']

        # Mapeo de días de la semana a números
        dias_semana = {
            'Lunes': 0,
            'Martes': 1,
            'Miércoles': 2,
            'Jueves': 3,
            'Viernes': 4,
            'Sábado': 5,
            'Domingo': 6
        }
        fecha_corresponde = False
        for dia_semana in dia_semana_seleccionados:
            dia_semana_num = dias_semana[dia_semana]
            # Calcular la fecha correspondiente al día de la semana seleccionado
            fecha_correspondiente = calculate_start_date(dia_semana_num, fecha_inicio)

            if fecha_correspondiente == fecha_inicio:
                fecha_corresponde = True
                break

        if not fecha_corresponde:
            raise forms.ValidationError("La fecha de inicio no corresponde a ninguno de los días seleccionados.")

        return fecha_inicio

class AsignacionEstudianteForm(forms.ModelForm):
    class Meta:
        model = AsignacionEstudiante
        fields = ['estudiante']
