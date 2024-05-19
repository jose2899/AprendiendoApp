from django import forms
from app.bitacora.models import Bitacora, NuevaBitacora
from app.usuarios.usuario.models import Estudiante
from app.planificaciones.models import Planificacion
from app.terapiass.models import Diagnostico

class BitacoraForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = ['estudiante', 'planificacion', 'diagnostico']
        widgets = {
            'estudiante':forms.Select(attrs={'class': 'form-control'}),
            'planificacion':forms.Select(attrs={'class': 'form-control'}),
            'diagnostico':forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BitacoraForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para el estudiante
        self.fields['estudiante'].queryset = Estudiante.objects.all()

    def __init__(self, *args, **kwargs):
        super(BitacoraForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para la planificacion
        self.fields['planificacion'].queryset = Planificacion.objects.all()

    def __init__(self, *args, **kwargs):
        super(BitacoraForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para la planificacion
        self.fields['diagnostico'].queryset = Diagnostico.objects.all()


class NuevaBitacoraForm(forms.ModelForm):
    class Meta:
        model = NuevaBitacora
        exclude = ['bitacora']
        fields = ['fecha', 'observacion_conducta', 'temas_trabajados', 'avance',
                  'firma_terapeuta', 'revisado_por', 'asistencias']
        labels = {
            'fecha': 'Fecha',
            'observacion_conducta': 'Observación de Conducta',
            'temas_trabajados': 'Temas Trabajados',
            'avance': 'Avance',
            'firma_terapeuta': 'Firma Terapeuta',
            'revisado_por': 'Revisado Por',
            'asistencias': 'asistencias'
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacion_conducta': forms.Select(attrs={'class': 'form-control'}),
            'temas_trabajados': forms.TextInput(attrs={'class': 'form-control'}),
            'avance': forms.Select(attrs={'class': 'form-control'}),
            'firma_terapeuta': forms.TextInput(attrs={'class': 'form-control'}),
            'revisado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'asistencias': forms.Select(attrs={'class': 'form-control'}),
        }