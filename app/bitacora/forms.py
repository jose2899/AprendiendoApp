from django import forms
from app.bitacora.models import Bitacora
from app.usuarios.usuario.models import Estudiante
from app.planificaciones.models import Planificacion

class BitacoraForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = ['estudiante', 'planificacion', 'diagnostico', 'fecha', 'observacion_conducta', 'temas_trabajados', 'avance',
                  'firma_terapeuta', 'revisado_por']
        labels = {
            'diagnostico': 'Diagnostico',
            'fecha': 'Fecha',
            'observacion_conducta': 'Observación de Conducta',
            'temas_trabajados': 'Temas Trabajados',
            'avance': 'Avance',
            'firma_terapeuta': 'Firma Terapeuta',
            'revisado_por': 'Revisado Por'
        }
        widgets = {
            'estudiante':forms.Select(attrs={'class': 'form-control'}),
            'planificacion':forms.Select(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacion_conducta': forms.TextInput(attrs={'class': 'form-control'}),
            'temas_trabajados': forms.TextInput(attrs={'class': 'form-control'}),
            'avance': forms.TextInput(attrs={'class': 'form-control'}),
            'firma_terapeuta': forms.TextInput(attrs={'class': 'form-control'}),
            'revisado_por': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BitacoraForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para el estudiante
        self.fields['estudiante'].queryset = Estudiante.objects.all()

    def __init__(self, *args, **kwargs):
        super(BitacoraForm, self).__init__(*args, **kwargs)
        # Agregar un campo de selección para la planificacion
        self.fields['planificacion'].queryset = Planificacion.objects.all()