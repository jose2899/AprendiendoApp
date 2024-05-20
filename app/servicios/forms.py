from django import forms
from app.servicios.models import Paquete
<<<<<<< HEAD
from app.usuarios.usuario.models import Representante, Estudiante
=======
from app.usuarios.usuario.models import Representante
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c

class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
<<<<<<< HEAD
        fields = ['horas', 'representante', 'servicios', 'estudiante']
=======
        fields = ['horas', 'representante', 'servicios']
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c
        widgets = {
            'servicios': forms.TextInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        servicio_id = kwargs.pop('servicio_id')
        super(PaqueteForm, self).__init__(*args, **kwargs)
        self.fields['representante'].queryset = Representante.objects.all()
        self.fields['servicios'].initial = servicio_id
<<<<<<< HEAD
        self.fields['estudiante'].queryset = Estudiante.objects.all()
=======
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c

  