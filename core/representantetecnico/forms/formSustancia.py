from django.forms import *

from core.representantetecnico.models import Sustancia


class SustanciaForm(ModelForm):

    class Meta:
        model = Sustancia
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'autofocus': 'true'
            }),
            'unidad_medida': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'descripcion': Textarea(attrs={
                'class': 'form-control',
                'rows': "5"
            }),
            'cupo_autorizado': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cupo autorizado de sustancia'
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
