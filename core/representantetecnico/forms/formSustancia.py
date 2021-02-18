from django.forms import *

from core.bodega.models import Sustancia


class SustanciaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sustancia
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'autofocus': 'true'
            }),
            'descripcion': TextInput(attrs={
                'class': 'form-control'
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
