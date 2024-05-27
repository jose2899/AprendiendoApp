from django import forms
from app.horarios.models import Asistencia


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['asistencia']
        widgets = {
            'asistencia': forms.CheckboxInput(),
        }