from django import forms
from app.servicios.models import Paquete
from app.usuarios.usuario.models import Representante

class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ['horas', 'representante', 'servicios']
        widgets = {
            'servicios': forms.TextInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        servicio_id = kwargs.pop('servicio_id')
        super(PaqueteForm, self).__init__(*args, **kwargs)
        self.fields['representante'].queryset = Representante.objects.all()
        self.fields['servicios'].initial = servicio_id

  