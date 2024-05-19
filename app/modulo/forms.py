from django import forms
class ModeloForm(forms.Form):
    modelo_pkl = forms.FileField(label='Seleccionar archivo del modelo (.pkl)')